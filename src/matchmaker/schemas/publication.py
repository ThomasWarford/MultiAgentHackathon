"""Researcher and publication models — Stage 1 ingestion handoff."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PublicationSource = Literal["local", "semantic_scholar", "google_scholar"]


class Publication(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Stable hash of (source, source_id) or filename slug.")
    title: str
    abstract: str | None = None
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    doi: str | None = None
    source: PublicationSource
    source_id: str = Field(description="Filename for local; paperId/scholar_id otherwise.")
    full_text_md: str | None = None


class ResearcherProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    researcher_id: str = Field(description="Slug, e.g. 'csanyi'.")
    display_name: str
    affiliation: str | None = None
    publications: list[Publication]
