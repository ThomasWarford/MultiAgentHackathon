"""Researcher-Derived Prompts — Stage 5 input."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ResearcherPrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    researcher_id: str
    current_focus: str = Field(description="What they're working on right now.")
    recent_milestones: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list, description="Things they're stuck on.")
    free_text: str | None = None
