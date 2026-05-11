"""Shared runtime entry points for matchmaker runs."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Optional

from matchmaker.agents.llm import OpenAIClient
from matchmaker.config import load_settings
from matchmaker.ingestion import LocalCorpusSource
from matchmaker.io import render_final_report, write_artifact
from matchmaker.logging import get_logger
from matchmaker.orchestrator import GraphContext, build_graph
from matchmaker.refinement import build_refinement_stack
from matchmaker.schemas import PipelineState


async def run_match_async(
    *,
    researcher_a: str,
    researcher_b: str,
    prompts_dir: Optional[Path],
    backend: Optional[str],
    papers_dir: Optional[Path],
    outputs_dir: Optional[Path],
    run_id: Optional[str],
) -> Path:
    log = get_logger(__name__)
    settings = load_settings()
    if backend:
        settings = settings.model_copy(update={"refinement_backend": backend})  # type: ignore[arg-type]

    effective_papers_dir = papers_dir or settings.papers_dir
    effective_prompts_dir = prompts_dir or settings.prompts_input_dir
    effective_outputs_dir = outputs_dir or settings.outputs_dir
    rid = run_id or f"run_{uuid.uuid4().hex[:8]}"

    source = LocalCorpusSource(effective_papers_dir)

    if settings.refinement_backend in {"mock"}:
        llm: OpenAIClient | None = None
    else:
        llm = OpenAIClient(
            api_key=settings.openai_api_key,
            cost_ceiling_usd=settings.cost_ceiling_usd,
        )

    # Stages 1-6 always need an LLM (unless backend is "mock" AND we also mock those).
    # In MVP the routing portion is real OpenAI; only refinement is swappable.
    if llm is None and settings.refinement_backend == "mock":
        llm = OpenAIClient(
            api_key=settings.openai_api_key,
            cost_ceiling_usd=settings.cost_ceiling_usd,
        )

    stack = build_refinement_stack(settings, llm=llm)

    ctx = GraphContext(
        settings=settings,
        llm=llm,
        source=source,
        stack=stack,
        researcher_a_id=researcher_a,
        researcher_b_id=researcher_b,
        prompts_dir=effective_prompts_dir,
    )
    graph = build_graph(ctx)

    initial = PipelineState(run_id=rid)
    log.info("run.start", run_id=rid, a=researcher_a, b=researcher_b, backend=settings.refinement_backend)

    final_dict = await graph.ainvoke(
        initial.model_dump(),
        config={"recursion_limit": 50},
    )
    final = PipelineState.model_validate(final_dict)
    final.token_spend_usd = llm.spend.usd

    write_all_artifacts(effective_outputs_dir, rid, final)

    report = render_final_report(final)
    report_path = effective_outputs_dir / "report" / f"{rid}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    log.info(
        "run.done",
        run_id=rid,
        report=str(report_path),
        token_spend_usd=round(final.token_spend_usd, 4),
    )
    return report_path


def write_all_artifacts(outputs_dir: Path, run_id: str, state: PipelineState) -> None:
    write_artifact(
        outputs_dir, "01_publications", run_id,
        {"profile_a": state.profile_a, "profile_b": state.profile_b},
    )
    write_artifact(
        outputs_dir, "02_backgrounds", run_id,
        {"background_a": state.background_a, "background_b": state.background_b},
    )
    write_artifact(
        outputs_dir, "03_dimensional", run_id,
        {"dimensions_a": state.dimensions_a, "dimensions_b": state.dimensions_b},
    )
    if state.matrix:
        write_artifact(outputs_dir, "04_matrix", run_id, state.matrix)
    write_artifact(
        outputs_dir, "05_hypotheses", run_id,
        {"hypotheses": state.hypotheses, "prompt_a": state.prompt_a, "prompt_b": state.prompt_b},
    )
    write_artifact(
        outputs_dir, "06_critiques", run_id,
        state.critique_histories,
    )
    write_artifact(
        outputs_dir, "07_refined", run_id,
        {"refined_hypotheses": state.refined_hypotheses},
    )
    if state.ranking:
        write_artifact(outputs_dir, "08_ranking", run_id, state.ranking)


__all__ = ["run_match_async", "write_all_artifacts"]
