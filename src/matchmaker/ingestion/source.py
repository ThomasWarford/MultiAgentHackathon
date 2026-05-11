"""Abstract Source — every ingestion backend implements this single method.

Live scrapers (SemanticScholarSource, GoogleScholarSource) come in phase 2
behind the same interface, so swapping requires no orchestrator changes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from matchmaker.schemas import ResearcherProfile


class Source(ABC):
    @abstractmethod
    async def fetch(self, researcher_id: str) -> ResearcherProfile:
        """Return a fully populated ResearcherProfile for the given researcher."""
