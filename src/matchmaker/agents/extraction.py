"""Stage 3 — DimensionalExtractor.

One parameterized agent for all three dimensions (Methods / Open Questions /
Stakes). Difference between dimensions is the prompt template only; the
schema and structured-output path are shared.

Orchestrator runs three of these in parallel via asyncio.gather.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents._corpus import format_publications_block
from matchmaker.agents.llm import OpenAIClient
from matchmaker.logging import get_logger
from matchmaker.prompts import render
from matchmaker.schemas import (
    Dim,
    DimensionalSummary,
    ResearcherBackground,
    ResearcherProfile,
    SummaryItem,
)

log = get_logger(__name__)


_PROMPT_BY_DIM: dict[Dim, str] = {
    "methods": "methods",
    "open_questions": "open_questions",
    "stakes": "stakes",
}


class _ItemsOutput(BaseModel):
    """Internal — researcher_id and dimension are bound by the caller."""

    model_config = ConfigDict(extra="forbid")

    items: list[SummaryItem] = Field(description="5-10 items for the requested dimension.")


class DimensionalExtractor:
    def __init__(self, llm: OpenAIClient, model: str, dimension: Dim) -> None:
        self._llm = llm
        self._model = model
        self._dim: Dim = dimension

    async def run(
        self,
        profile: ResearcherProfile,
        background: ResearcherBackground,
    ) -> DimensionalSummary:
        prompt = render(
            _PROMPT_BY_DIM[self._dim],
            researcher_id=profile.researcher_id,
            display_name=profile.display_name,
            background_narrative=background.narrative,
            publications_block=format_publications_block(profile),
        )
        log.info(
            "agent.extraction.start",
            researcher_id=profile.researcher_id,
            dimension=self._dim,
        )
        out = await self._llm.structured(
            model=self._model,
            system=(
                "You extract precise, evidence-grounded summaries from research corpora. "
                "Cite only Publication.id values present in the provided block."
            ),
            user=prompt,
            response_model=_ItemsOutput,
            temperature=1.0,
            max_tokens=3072,
        )
        summary = DimensionalSummary(
            researcher_id=profile.researcher_id,
            dimension=self._dim,
            items=out.items,
        )
        log.info(
            "agent.extraction.done",
            researcher_id=profile.researcher_id,
            dimension=self._dim,
            n_items=len(summary.items),
        )
        return summary
