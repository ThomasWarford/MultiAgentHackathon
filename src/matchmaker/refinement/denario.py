"""Denario stubs. The proprietary Cambridge endpoints will fill these in.

Each class implements the Protocol shape so an `isinstance(obj, Protocol)`
check passes at construction time — only the method bodies are unimplemented.
This is the swap-day contract: when Denario ships, replace the bodies, run
tests/test_refinement_protocols.py against the real classes, and flip
`config.refinement_backend = "denario"`.
"""

from __future__ import annotations

from matchmaker.schemas import (
    Critique,
    CritiqueHistory,
    Hypothesis,
    Ranking,
    RefinedHypothesis,
)


class DenarioReviewer:
    reviewer_id: str = "denario-v1"

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key

    async def review(self, hypothesis: Hypothesis, history: CritiqueHistory) -> Critique:
        raise NotImplementedError("Plug in Denario reviewer endpoint.")


class DenarioRefiner:
    refiner_id: str = "denario-v1"

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key

    async def refine(
        self,
        hypothesis: Hypothesis,
        critique: Critique,
        history: CritiqueHistory,
    ) -> RefinedHypothesis:
        raise NotImplementedError("Plug in Denario refiner endpoint.")


class DenarioRanker:
    ranker_id: str = "denario-v1"

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key

    async def rank(self, hypotheses: list[RefinedHypothesis]) -> Ranking:
        raise NotImplementedError("Plug in Denario ranker endpoint.")
