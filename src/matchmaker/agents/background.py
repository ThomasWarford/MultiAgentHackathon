"""Stage 2 — ResearcherBackgroundAgent.

Distills a ResearcherProfile into a narrative ResearcherBackground that the
three extraction agents (Stage 3) consume.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents._corpus import format_publications_block
from matchmaker.agents.llm import OpenAIClient
from matchmaker.logging import get_logger
from matchmaker.prompts import render
from matchmaker.schemas import ResearcherBackground, ResearcherProfile

log = get_logger(__name__)


class _BackgroundOutput(BaseModel):
    """Internal response shape; researcher_id is bound by the caller."""

    model_config = ConfigDict(extra="forbid")

    narrative: str = Field(description="3-6 paragraph synthesis of the researcher's program.")
    keywords: list[str] = Field(description="8-15 substantive keywords.")


class ResearcherBackgroundAgent:
    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model

    async def run(self, profile: ResearcherProfile) -> ResearcherBackground:
        prompt = render(
            "background",
            researcher_id=profile.researcher_id,
            display_name=profile.display_name,
            publications_block=format_publications_block(profile),
        )
        log.info(
            "agent.background.start",
            researcher_id=profile.researcher_id,
            n_publications=len(profile.publications),
        )
        out = await self._llm.structured(
            model=self._model,
            system="You produce faithful, specific, evidence-grounded research syntheses.",
            user=prompt,
            response_model=_BackgroundOutput,
            temperature=0.0,
            max_tokens=2048,
        )
        background = ResearcherBackground(
            researcher_id=profile.researcher_id,
            narrative=out.narrative,
            keywords=out.keywords,
        )
        log.info(
            "agent.background.done",
            researcher_id=profile.researcher_id,
            keyword_count=len(background.keywords),
        )
        return background
