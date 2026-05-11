"""Stage 6 — HypothesesAgent.

Synthesizes both researchers' backgrounds, current ResearcherPrompts, and the
9-cell CrossFactorialMatrix into 3-7 candidate collaborative Hypotheses.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents.llm import OpenAIClient
from matchmaker.logging import get_logger
from matchmaker.prompts import render
from matchmaker.schemas import (
    CrossFactorialMatrix,
    Dim,
    Hypothesis,
    ResearcherBackground,
    ResearcherPrompt,
)

log = get_logger(__name__)


class _CellRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dim_a: Dim
    dim_b: Dim


class _HypothesisDraft(BaseModel):
    """Internal — leverages is converted to (Dim, Dim) tuples post-parse."""

    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    title: str
    statement: str = Field(description="1-2 sentence falsifiable claim.")
    mechanism: str = Field(description="How the collaboration would actually work.")
    leverages: list[_CellRef] = Field(
        description="ConnectionCells this hypothesis draws on."
    )
    addresses_prompts: list[str] = Field(
        description="researcher_ids whose ResearcherPrompts this addresses."
    )
    confidence: float = Field(ge=0.0, le=1.0)


class _HypothesesOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hypotheses: list[_HypothesisDraft] = Field(description="3-7 candidate hypotheses.")


class _DuplicateGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    keep_hypothesis_id: str = Field(description="The best representative to keep.")
    duplicate_hypothesis_ids: list[str] = Field(
        description="Other hypothesis_ids that are semantically the same."
    )
    rationale: str = Field(
        description="Brief reason these hypotheses express the same underlying claim."
    )


class _HypothesisFilterOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    keep_hypothesis_ids: list[str] = Field(
        description="Unique hypothesis_ids to keep, in preferred output order."
    )
    duplicate_groups: list[_DuplicateGroup] = Field(default_factory=list)


def _format_bullets(items: list[str], empty: str = "(none provided)") -> str:
    if not items:
        return empty
    return "\n".join(f"- {x}" for x in items)


def _format_matrix(matrix: CrossFactorialMatrix) -> str:
    parts: list[str] = []
    for c in matrix.cells:
        parts.append(
            f"### [{c.dim_a} × {c.dim_b}] type={c.connection_type} "
            f"novelty={c.novelty_score:.2f} confidence={c.confidence:.2f}\n"
            f"- A items: {', '.join(c.items_a) or '(none)'}\n"
            f"- B items: {', '.join(c.items_b) or '(none)'}\n"
            f"- Rationale: {c.rationale}"
        )
    return "\n\n".join(parts)


def _format_hypotheses_for_filter(hypotheses: list[Hypothesis]) -> str:
    parts: list[str] = []
    for h in hypotheses:
        leverages = ", ".join(f"{a} x {b}" for a, b in h.leverages_cells) or "(none)"
        addresses = ", ".join(h.addresses_prompts) or "(none)"
        parts.append(
            f"## {h.hypothesis_id}\n"
            f"Title: {h.title}\n"
            f"Statement: {h.statement}\n"
            f"Mechanism: {h.mechanism}\n"
            f"Leverages: {leverages}\n"
            f"Addresses: {addresses}\n"
            f"Confidence: {h.confidence:.2f}"
        )
    return "\n\n".join(parts)


def _filter_by_keep_ids(
    hypotheses: list[Hypothesis], keep_hypothesis_ids: list[str]
) -> list[Hypothesis]:
    by_id = {h.hypothesis_id: h for h in hypotheses}
    unique: list[Hypothesis] = []
    seen: set[str] = set()
    for hypothesis_id in keep_hypothesis_ids:
        if hypothesis_id in by_id and hypothesis_id not in seen:
            unique.append(by_id[hypothesis_id])
            seen.add(hypothesis_id)
    return unique


def _drop_duplicate_ids(hypotheses: list[Hypothesis]) -> list[Hypothesis]:
    unique: list[Hypothesis] = []
    seen: set[str] = set()
    for hypothesis in hypotheses:
        if hypothesis.hypothesis_id in seen:
            continue
        unique.append(hypothesis)
        seen.add(hypothesis.hypothesis_id)
    return unique


class HypothesisFilterAgent:
    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model

    async def run(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        hypotheses = _drop_duplicate_ids(hypotheses)
        if len(hypotheses) <= 1:
            return hypotheses

        log.info("agent.hypothesis_filter.start", n_hypotheses=len(hypotheses))
        out = await self._llm.structured(
            model=self._model,
            system=(
                "You are a precise research-hypothesis deduplication agent. "
                "You identify semantic duplicates, not merely matching wording."
            ),
            user=(
                "Filter this candidate set to unique collaborative hypotheses.\n\n"
                "Treat hypotheses as duplicates when they propose the same underlying "
                "falsifiable claim and collaboration mechanism, even if the wording, "
                "title, or slug differs. Keep separate hypotheses that share a topic "
                "but test a different claim, require a different dataset/experiment, "
                "or have a materially different mechanism.\n\n"
                "Prefer keeping the stronger, more specific, more falsifiable member "
                "of each duplicate group. Return only existing hypothesis_ids.\n\n"
                f"{_format_hypotheses_for_filter(hypotheses)}"
            ),
            response_model=_HypothesisFilterOutput,
            temperature=0.0,
            max_tokens=2048,
        )

        unique = _filter_by_keep_ids(hypotheses, out.keep_hypothesis_ids)
        if not unique:
            log.info(
                "agent.hypothesis_filter.invalid_output",
                keep_hypothesis_ids=out.keep_hypothesis_ids,
            )
            return hypotheses

        log.info(
            "agent.hypothesis_filter.done",
            n_hypotheses=len(unique),
            n_duplicates_dropped=len(hypotheses) - len(unique),
            n_duplicate_groups=len(out.duplicate_groups),
        )
        return unique


class HypothesesAgent:
    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model
        self._filter = HypothesisFilterAgent(llm=llm, model=model)

    async def run(
        self,
        *,
        background_a: ResearcherBackground,
        background_b: ResearcherBackground,
        prompt_a: ResearcherPrompt,
        prompt_b: ResearcherPrompt,
        matrix: CrossFactorialMatrix,
        display_a: str,
        display_b: str,
    ) -> list[Hypothesis]:
        rendered = render(
            "hypotheses",
            display_a=display_a,
            display_b=display_b,
            researcher_a_id=background_a.researcher_id,
            researcher_b_id=background_b.researcher_id,
            background_a=background_a.narrative,
            background_b=background_b.narrative,
            current_focus_a=prompt_a.current_focus,
            current_focus_b=prompt_b.current_focus,
            milestones_a_block=_format_bullets(prompt_a.recent_milestones),
            milestones_b_block=_format_bullets(prompt_b.recent_milestones),
            blockers_a_block=_format_bullets(prompt_a.blockers),
            blockers_b_block=_format_bullets(prompt_b.blockers),
            matrix_block=_format_matrix(matrix),
        )
        log.info(
            "agent.hypotheses.start",
            researcher_a=background_a.researcher_id,
            researcher_b=background_b.researcher_id,
        )
        out = await self._llm.structured(
            model=self._model,
            system=(
                "You propose concrete, falsifiable collaborative research hypotheses "
                "grounded in evidence. Refuse vague brainstorms."
            ),
            user=rendered,
            response_model=_HypothesesOutput,
            temperature=1.0,
            max_tokens=4096,
        )
        hypotheses = [
            Hypothesis(
                hypothesis_id=d.hypothesis_id,
                title=d.title,
                statement=d.statement,
                mechanism=d.mechanism,
                leverages_cells=[(c.dim_a, c.dim_b) for c in d.leverages],
                addresses_prompts=d.addresses_prompts,
                confidence=d.confidence,
            )
            for d in out.hypotheses
        ]
        unique_hypotheses = await self._filter.run(hypotheses)
        log.info(
            "agent.hypotheses.done",
            n_hypotheses=len(unique_hypotheses),
            n_duplicates_dropped=len(hypotheses) - len(unique_hypotheses),
        )
        return unique_hypotheses
