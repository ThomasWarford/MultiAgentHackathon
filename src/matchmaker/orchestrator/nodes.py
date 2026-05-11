"""Async node functions for the LangGraph pipeline.

Each `make_*_node(ctx)` returns the actual node coroutine, closing over the
GraphContext (which carries the LLM client, settings, ingestion source, and
refinement stack). Nodes return *partial state dicts* — LangGraph merges them
into the PipelineState by field name.

The refine→review loop is implemented INSIDE the refine_loop node (per-
hypothesis asyncio.gather over a Python while loop), not as LangGraph
conditional edges. That keeps the graph linear and lets each hypothesis run
its own bounded loop independently.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from matchmaker.agents.background import ResearcherBackgroundAgent
from matchmaker.agents.cross_factorial import CrossFactorialAgent
from matchmaker.agents.extraction import DimensionalExtractor
from matchmaker.agents.hypotheses import HypothesesAgent
from matchmaker.ingestion import load_researcher_prompt
from matchmaker.logging import get_logger
from matchmaker.schemas import (
    DIMS,
    CritiqueHistory,
    Hypothesis,
    PipelineState,
    RefinedHypothesis,
)

if TYPE_CHECKING:
    from matchmaker.orchestrator.graph import GraphContext

log = get_logger(__name__)


# ---- ingestion ----


def make_ingest_node(ctx: "GraphContext"):
    async def ingest(state: PipelineState) -> dict[str, Any]:
        log.info("node.ingest.start", run_id=state.run_id)
        profile_a, profile_b = await asyncio.gather(
            ctx.source.fetch(ctx.researcher_a_id),
            ctx.source.fetch(ctx.researcher_b_id),
        )
        return {"profile_a": profile_a, "profile_b": profile_b}

    return ingest


# ---- background ----


def make_background_node(ctx: "GraphContext"):
    agent = ResearcherBackgroundAgent(llm=ctx.llm, model=ctx.settings.model_background)

    async def background(state: PipelineState) -> dict[str, Any]:
        assert state.profile_a and state.profile_b
        log.info("node.background.start", run_id=state.run_id)
        bg_a, bg_b = await asyncio.gather(
            agent.run(state.profile_a),
            agent.run(state.profile_b),
        )
        return {"background_a": bg_a, "background_b": bg_b}

    return background


# ---- extraction (Stage 3 fan-out) ----


def make_extraction_node(ctx: "GraphContext"):
    extractors = {
        dim: DimensionalExtractor(
            llm=ctx.llm, model=ctx.settings.model_extraction, dimension=dim
        )
        for dim in DIMS
    }

    async def extract(state: PipelineState) -> dict[str, Any]:
        assert state.profile_a and state.profile_b
        assert state.background_a and state.background_b
        log.info("node.extract.start", run_id=state.run_id)
        coros = []
        for dim in DIMS:
            coros.append(extractors[dim].run(state.profile_a, state.background_a))
        for dim in DIMS:
            coros.append(extractors[dim].run(state.profile_b, state.background_b))
        results = await asyncio.gather(*coros)
        dims_a = list(results[: len(DIMS)])
        dims_b = list(results[len(DIMS):])
        return {"dimensions_a": dims_a, "dimensions_b": dims_b}

    return extract


# ---- cross-factorial (Stage 4) ----


def make_cross_factorial_node(ctx: "GraphContext"):
    agent = CrossFactorialAgent(llm=ctx.llm, model=ctx.settings.model_cross_factorial)

    async def cross_factorial(state: PipelineState) -> dict[str, Any]:
        assert state.profile_a and state.profile_b
        log.info("node.cross_factorial.start", run_id=state.run_id)
        matrix = await agent.run(
            state.profile_a, state.dimensions_a,
            state.profile_b, state.dimensions_b,
        )
        return {"matrix": matrix}

    return cross_factorial


# ---- prompts (Stage 5) ----


def make_load_prompts_node(ctx: "GraphContext"):
    async def load_prompts(state: PipelineState) -> dict[str, Any]:
        log.info("node.load_prompts.start", run_id=state.run_id)
        # I/O is synchronous and small; no need for to_thread.
        prompt_a = load_researcher_prompt(ctx.prompts_dir, ctx.researcher_a_id)
        prompt_b = load_researcher_prompt(ctx.prompts_dir, ctx.researcher_b_id)
        return {"prompt_a": prompt_a, "prompt_b": prompt_b}

    return load_prompts


# ---- hypotheses (Stage 6) ----


def make_hypotheses_node(ctx: "GraphContext"):
    agent = HypothesesAgent(llm=ctx.llm, model=ctx.settings.model_hypotheses)

    async def hypotheses(state: PipelineState) -> dict[str, Any]:
        assert state.background_a and state.background_b
        assert state.prompt_a and state.prompt_b
        assert state.matrix and state.profile_a and state.profile_b
        log.info("node.hypotheses.start", run_id=state.run_id)
        hs = await agent.run(
            background_a=state.background_a,
            background_b=state.background_b,
            prompt_a=state.prompt_a,
            prompt_b=state.prompt_b,
            matrix=state.matrix,
            display_a=state.profile_a.display_name,
            display_b=state.profile_b.display_name,
        )
        return {"hypotheses": hs}

    return hypotheses


# ---- refine loop (Stages 7) ----


async def _refine_one(
    hypothesis: Hypothesis,
    ctx: "GraphContext",
) -> tuple[RefinedHypothesis, CritiqueHistory]:
    """Run the review→refine cycle for ONE hypothesis with early-exit on accept."""
    history = CritiqueHistory(hypothesis_id=hypothesis.hypothesis_id)
    current: Hypothesis = hypothesis
    max_iter = ctx.settings.max_iterations

    for _ in range(max_iter):
        critique = await ctx.stack.reviewer.review(current, history)
        history.critiques.append(critique)
        if critique.severity == "accept":
            break
        prior = CritiqueHistory(
            hypothesis_id=history.hypothesis_id,
            critiques=history.critiques[:-1],
        )
        current = await ctx.stack.refiner.refine(current, critique, prior)

    if isinstance(current, RefinedHypothesis):
        return current, history

    # Accepted on first review with no refinement performed — promote to RefinedHypothesis.
    refined = RefinedHypothesis(
        hypothesis_id=current.hypothesis_id,
        title=current.title,
        statement=current.statement,
        mechanism=current.mechanism,
        leverages_cells=current.leverages_cells,
        addresses_prompts=current.addresses_prompts,
        confidence=current.confidence,
        revision_notes="Accepted on first review with no revisions required.",
        prior_critique_iterations=[c.iteration for c in history.critiques],
    )
    return refined, history


def make_refine_loop_node(ctx: "GraphContext"):
    async def refine_loop(state: PipelineState) -> dict[str, Any]:
        log.info(
            "node.refine_loop.start",
            run_id=state.run_id,
            n_hypotheses=len(state.hypotheses),
            max_iterations=ctx.settings.max_iterations,
        )
        results = await asyncio.gather(
            *[_refine_one(h, ctx) for h in state.hypotheses]
        )
        refined = [r for r, _ in results]
        histories = {h.hypothesis_id: h for _, h in results}
        max_iter = max((len(h.critiques) for h in histories.values()), default=0)
        return {
            "refined_hypotheses": refined,
            "critique_histories": histories,
            "iteration": max_iter,
        }

    return refine_loop


# ---- rank (Stage 8) ----


def make_rank_node(ctx: "GraphContext"):
    async def rank(state: PipelineState) -> dict[str, Any]:
        log.info("node.rank.start", run_id=state.run_id, n=len(state.refined_hypotheses))
        ranking = await ctx.stack.ranker.rank(state.refined_hypotheses)
        return {"ranking": ranking}

    return rank
