"""The Denario seam.

These Protocols are the *only* contract between the orchestrator and any
refinement backend. No LangGraph types, no orchestrator state — every call
takes Pydantic models in and out. CritiqueHistory is threaded explicitly by
the caller so backends remain stateless from the orchestrator's view.

Any backend implementation (mock, local-Claude, Denario) must satisfy these
Protocols; the contract test in tests/test_refinement_protocols.py asserts it.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from matchmaker.schemas import (
    Critique,
    CritiqueHistory,
    Hypothesis,
    Ranking,
    RefinedHypothesis,
)


@runtime_checkable
class ReviewerProtocol(Protocol):
    reviewer_id: str

    async def review(
        self, hypothesis: Hypothesis, history: CritiqueHistory
    ) -> Critique: ...


@runtime_checkable
class RefinerProtocol(Protocol):
    refiner_id: str

    async def refine(
        self,
        hypothesis: Hypothesis,
        critique: Critique,
        history: CritiqueHistory,
    ) -> RefinedHypothesis: ...


@runtime_checkable
class RankerProtocol(Protocol):
    ranker_id: str

    async def rank(self, hypotheses: list[RefinedHypothesis]) -> Ranking: ...
