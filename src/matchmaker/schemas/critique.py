"""Reviewer outputs — Stage 7 critique types crossing the Denario boundary."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CritiqueSeverity = Literal["block", "suggest", "accept"]


class Critique(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    iteration: int = Field(ge=0)
    severity: CritiqueSeverity = Field(
        description="'accept' triggers early-exit from the refinement loop.",
    )
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggested_revisions: list[str] = Field(default_factory=list)
    reviewer_id: str = Field(description="e.g. 'local-openai', 'denario-v1'.")


class CritiqueHistory(BaseModel):
    """Threaded explicitly through Protocol calls — no hidden state."""

    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    critiques: list[Critique] = Field(default_factory=list)

    def latest(self) -> Critique | None:
        return self.critiques[-1] if self.critiques else None
