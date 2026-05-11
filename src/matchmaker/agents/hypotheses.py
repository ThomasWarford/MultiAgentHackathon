"""Stage 6 — HypothesesAgent.

Synthesizes both researchers' backgrounds, current ResearcherPrompts, and the
9-cell CrossFactorialMatrix into 3-7 candidate collaborative Hypotheses.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents.llm import AnthropicClient
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


class HypothesesAgent:
    def __init__(self, llm: AnthropicClient, model: str) -> None:
        self._llm = llm
        self._model = model

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
            temperature=0.7,
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
        log.info(
            "agent.hypotheses.done",
            n_hypotheses=len(hypotheses),
        )
        return hypotheses
