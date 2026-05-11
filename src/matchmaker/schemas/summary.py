"""Dimensional summaries — Stages 2 and 3 outputs."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Dim = Literal["methods", "open_questions", "stakes"]


class SummaryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(description="Stable within a DimensionalSummary.")
    title: str = Field(description="5-12 words.")
    description: str = Field(description="2-4 sentences.")
    evidence: list[str] = Field(
        default_factory=list,
        description="Publication.id values backing this item.",
    )


class DimensionalSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    researcher_id: str
    dimension: Dim
    items: list[SummaryItem] = Field(description="Target 5-10 per dimension.")


class ResearcherBackground(BaseModel):
    """Stage 2 narrative profile — feeds the extraction agents."""

    model_config = ConfigDict(extra="forbid")

    researcher_id: str
    narrative: str = Field(description="3-6 paragraph synthesis of trajectory and worldview.")
    keywords: list[str] = Field(default_factory=list)
