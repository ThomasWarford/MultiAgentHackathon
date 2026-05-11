"""Collaborative hypotheses — Stage 6 synthesis output."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.schemas.summary import Dim


class Hypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    title: str
    statement: str = Field(description="1-2 sentence falsifiable claim.")
    mechanism: str = Field(description="How the collaboration would actually work.")
    leverages_cells: list[tuple[Dim, Dim]] = Field(
        default_factory=list,
        description="Which (dim_a, dim_b) ConnectionCells this draws on.",
    )
    addresses_prompts: list[str] = Field(
        default_factory=list,
        description="researcher_ids whose ResearcherPrompts this addresses.",
    )
    confidence: float = Field(ge=0.0, le=1.0)


class RefinedHypothesis(Hypothesis):
    """Output of the Refiner after consuming a Critique."""

    revision_notes: str = Field(description="What changed and why.")
    prior_critique_iterations: list[int] = Field(
        default_factory=list,
        description="Iteration numbers of critiques consumed.",
    )
