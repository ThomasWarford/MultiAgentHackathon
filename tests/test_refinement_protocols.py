"""Contract test for the Denario seam.

Every refinement backend must satisfy ReviewerProtocol / RefinerProtocol /
RankerProtocol. When Denario lands, this test must stay green against the
real Denario classes — green here = safe swap.
"""

from __future__ import annotations

import pytest

from matchmaker.refinement.denario import DenarioRanker, DenarioRefiner, DenarioReviewer
from matchmaker.refinement.mocks import MockRanker, MockRefiner, MockReviewer
from matchmaker.refinement.protocols import (
    RankerProtocol,
    RefinerProtocol,
    ReviewerProtocol,
)
from matchmaker.schemas import (
    Critique,
    CritiqueHistory,
    Hypothesis,
    RefinedHypothesis,
)


def _hypothesis(hid: str = "h1", confidence: float = 0.7) -> Hypothesis:
    return Hypothesis(
        hypothesis_id=hid,
        title=f"Hypothesis {hid}",
        statement="A claim.",
        mechanism="How it works.",
        leverages_cells=[("methods", "stakes")],
        addresses_prompts=["a"],
        confidence=confidence,
    )


class TestProtocolConformance:
    """Both mock and Denario backends must conform — even before Denario is wired."""

    def test_mock_reviewer_satisfies_protocol(self) -> None:
        assert isinstance(MockReviewer(), ReviewerProtocol)

    def test_mock_refiner_satisfies_protocol(self) -> None:
        assert isinstance(MockRefiner(), RefinerProtocol)

    def test_mock_ranker_satisfies_protocol(self) -> None:
        assert isinstance(MockRanker(), RankerProtocol)

    def test_denario_reviewer_satisfies_protocol(self) -> None:
        assert isinstance(DenarioReviewer("u", "k"), ReviewerProtocol)

    def test_denario_refiner_satisfies_protocol(self) -> None:
        assert isinstance(DenarioRefiner("u", "k"), RefinerProtocol)

    def test_denario_ranker_satisfies_protocol(self) -> None:
        assert isinstance(DenarioRanker("u", "k"), RankerProtocol)


class TestDenarioStubsRaise:
    """Stubs must raise NotImplementedError until Cambridge wires endpoints."""

    async def test_reviewer_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            await DenarioReviewer("u", "k").review(
                _hypothesis(), CritiqueHistory(hypothesis_id="h1")
            )

    async def test_refiner_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            await DenarioRefiner("u", "k").refine(
                _hypothesis(),
                Critique(
                    hypothesis_id="h1",
                    iteration=0,
                    severity="suggest",
                    reviewer_id="x",
                ),
                CritiqueHistory(hypothesis_id="h1"),
            )

    async def test_ranker_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            await DenarioRanker("u", "k").rank([])


class TestMockBehavior:
    """Mock outputs are deterministic — the orchestrator can run end-to-end."""

    async def test_reviewer_suggests_on_iter0_accepts_on_iter1(self) -> None:
        rev = MockReviewer()
        h = _hypothesis()
        first = await rev.review(h, CritiqueHistory(hypothesis_id="h1"))
        assert first.severity == "suggest"
        second = await rev.review(
            h, CritiqueHistory(hypothesis_id="h1", critiques=[first])
        )
        assert second.severity == "accept"

    async def test_refiner_returns_refined_hypothesis(self) -> None:
        rev = MockReviewer()
        ref = MockRefiner()
        h = _hypothesis()
        critique = await rev.review(h, CritiqueHistory(hypothesis_id="h1"))
        refined = await ref.refine(
            h, critique, CritiqueHistory(hypothesis_id="h1", critiques=[critique])
        )
        assert isinstance(refined, RefinedHypothesis)
        assert refined.hypothesis_id == "h1"

    async def test_ranker_sorts_by_confidence_descending(self) -> None:
        rev = MockReviewer()
        ref = MockRefiner()
        ranker = MockRanker()
        refineds = []
        for hid, conf in [("low", 0.2), ("high", 0.9), ("mid", 0.5)]:
            h = _hypothesis(hid=hid, confidence=conf)
            critique = await rev.review(h, CritiqueHistory(hypothesis_id=hid))
            refined = await ref.refine(
                h, critique, CritiqueHistory(hypothesis_id=hid, critiques=[critique])
            )
            refineds.append(refined)
        ranking = await ranker.rank(refineds)
        assert [r.hypothesis_id for r in ranking.items] == ["high", "mid", "low"]
        assert [r.rank for r in ranking.items] == [1, 2, 3]


class TestFactory:
    def test_mock_backend_builds_stack(self) -> None:
        from matchmaker.config import Settings
        from matchmaker.refinement import build_refinement_stack

        stack = build_refinement_stack(Settings(refinement_backend="mock"))
        assert isinstance(stack.reviewer, ReviewerProtocol)
        assert isinstance(stack.refiner, RefinerProtocol)
        assert isinstance(stack.ranker, RankerProtocol)

    def test_local_backend_requires_llm(self) -> None:
        from matchmaker.config import Settings
        from matchmaker.refinement import build_refinement_stack

        with pytest.raises(ValueError, match="AnthropicClient"):
            build_refinement_stack(Settings(refinement_backend="local"))

    def test_local_backend_builds_stack_with_llm(self) -> None:
        from matchmaker.agents.llm import AnthropicClient
        from matchmaker.config import Settings
        from matchmaker.refinement import build_refinement_stack

        llm = AnthropicClient(api_key="dummy", cost_ceiling_usd=1.0)
        stack = build_refinement_stack(Settings(refinement_backend="local"), llm=llm)
        assert isinstance(stack.reviewer, ReviewerProtocol)
        assert isinstance(stack.refiner, RefinerProtocol)
        assert isinstance(stack.ranker, RankerProtocol)

    def test_denario_backend_builds_stack(self) -> None:
        from matchmaker.config import Settings
        from matchmaker.refinement import build_refinement_stack

        stack = build_refinement_stack(
            Settings(
                refinement_backend="denario",
                DENARIO_BASE_URL="http://stub",
                DENARIO_API_KEY="k",
            )
        )
        assert isinstance(stack.reviewer, ReviewerProtocol)
