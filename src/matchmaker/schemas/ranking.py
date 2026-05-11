"""Ranking outputs — Stage 8 final artifact."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RankedHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    rank: int = Field(ge=1)
    composite_score: float = Field(ge=0.0, le=1.0)
    dimension_scores: dict[str, float] = Field(
        default_factory=dict,
        description="e.g. {'novelty':0.8, 'feasibility':0.6, 'stake_alignment':0.9}.",
    )
    justification: str


class Ranking(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[RankedHypothesis]
    methodology: str = Field(description="How the ranker weighed dimensions.")
    ranker_id: str
