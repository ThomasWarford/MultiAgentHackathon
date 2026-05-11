"""LocalLLM refinement implementations — exercise prompt-rendering and
output-binding paths with a mocked LLM."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from matchmaker.agents.ranking import (
    _DimensionScoresOutput,
    _RankedItemOutput,
    _RankingOutput,
    RankingAgent,
)
from matchmaker.refinement.local import (
    LocalLLMRanker,
    LocalLLMRefiner,
    LocalLLMReviewer,
    _CellRef,
    _CritiqueOutput,
    _RefinedOutput,
)
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


class _FakeLLM:
    def __init__(self, responses: list[BaseModel]) -> None:
        self._responses = list(responses)
        self.captured: list[dict[str, Any]] = []

    async def structured(self, **kwargs: Any) -> BaseModel:
        self.captured.append(kwargs)
        return self._responses.pop(0)


def _hyp() -> Hypothesis:
    return Hypothesis(
        hypothesis_id="h1",
        title="Hypothesis One",
        statement="X causes Y.",
        mechanism="By the mechanism.",
        leverages_cells=[("methods", "stakes")],
        addresses_prompts=["alice"],
        confidence=0.7,
    )


class TestProtocolConformance:
    def test_reviewer_satisfies_protocol(self) -> None:
        from matchmaker.agents.llm import OpenAIClient

        c = OpenAIClient(api_key="dummy", cost_ceiling_usd=1.0)
        assert isinstance(LocalLLMReviewer(c, "x"), ReviewerProtocol)

    def test_refiner_satisfies_protocol(self) -> None:
        from matchmaker.agents.llm import OpenAIClient

        c = OpenAIClient(api_key="dummy", cost_ceiling_usd=1.0)
        assert isinstance(LocalLLMRefiner(c, "x"), RefinerProtocol)

    def test_ranker_satisfies_protocol(self) -> None:
        from matchmaker.agents.llm import OpenAIClient

        c = OpenAIClient(api_key="dummy", cost_ceiling_usd=1.0)
        assert isinstance(RankingAgent(c, "x"), RankerProtocol)
        assert isinstance(LocalLLMRanker(c, "x"), RankerProtocol)


class TestReviewer:
    async def test_review_binds_hypothesis_id_and_iteration(self) -> None:
        llm = _FakeLLM(
            [
                _CritiqueOutput(
                    severity="suggest",
                    strengths=["good claim"],
                    weaknesses=["vague mechanism"],
                    suggested_revisions=["name the dataset"],
                )
            ]
        )
        rev = LocalLLMReviewer(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]
        h = _hyp()
        out = await rev.review(h, CritiqueHistory(hypothesis_id="h1"))
        assert out.hypothesis_id == "h1"
        assert out.iteration == 0
        assert out.reviewer_id == "local-openai"
        assert out.severity == "suggest"
        assert out.suggested_revisions == ["name the dataset"]

    async def test_iteration_index_increments_with_history(self) -> None:
        llm = _FakeLLM(
            [
                _CritiqueOutput(
                    severity="accept",
                    strengths=["ok"],
                    weaknesses=[],
                    suggested_revisions=[],
                )
            ]
        )
        rev = LocalLLMReviewer(llm=llm, model="x")  # type: ignore[arg-type]
        prior = Critique(
            hypothesis_id="h1",
            iteration=0,
            severity="suggest",
            reviewer_id="local-openai",
            suggested_revisions=["foo"],
        )
        out = await rev.review(
            _hyp(), CritiqueHistory(hypothesis_id="h1", critiques=[prior])
        )
        assert out.iteration == 1
        # Prompt must include the prior critique so the reviewer can avoid relitigating.
        assert "Iteration 0" in llm.captured[0]["user"]


class TestRefiner:
    async def test_refine_binds_hypothesis_id_and_threads_iterations(self) -> None:
        llm = _FakeLLM(
            [
                _RefinedOutput(
                    title="Refined Title",
                    statement="Refined statement.",
                    mechanism="Refined mechanism.",
                    leverages=[_CellRef(dim_a="methods", dim_b="open_questions")],
                    addresses_prompts=["alice", "bob"],
                    confidence=0.85,
                    revision_notes="Tightened claim.",
                )
            ]
        )
        ref = LocalLLMRefiner(llm=llm, model="x")  # type: ignore[arg-type]
        critique = Critique(
            hypothesis_id="h1",
            iteration=0,
            severity="suggest",
            reviewer_id="local-openai",
            suggested_revisions=["tighten"],
        )
        refined = await ref.refine(
            _hyp(), critique, CritiqueHistory(hypothesis_id="h1")
        )
        assert isinstance(refined, RefinedHypothesis)
        assert refined.hypothesis_id == "h1"
        assert refined.title == "Refined Title"
        assert refined.leverages_cells == [("methods", "open_questions")]
        assert refined.prior_critique_iterations == [0]


class TestRanker:
    async def test_rank_empty_short_circuits(self) -> None:
        llm = _FakeLLM([])  # never used
        ranker = LocalLLMRanker(llm=llm, model="x")  # type: ignore[arg-type]
        out = await ranker.rank([])
        assert out.items == []
        assert out.ranker_id == "local-openai"

    async def test_rank_returns_ordered_list(self) -> None:
        llm = _FakeLLM(
            [
                _RankingOutput(
                    items=[
                        _RankedItemOutput(
                            hypothesis_id="h2",
                            rank=1,
                            composite_score=0.9,
                            dimension_scores=_DimensionScoresOutput(
                                novelty=0.95,
                                feasibility=0.85,
                                falsifiability=0.9,
                                stake_alignment=0.8,
                                evidence_grounding=0.75,
                            ),
                            justification="strong on both.",
                        ),
                        _RankedItemOutput(
                            hypothesis_id="h1",
                            rank=2,
                            composite_score=0.6,
                            dimension_scores=_DimensionScoresOutput(
                                novelty=0.5,
                                feasibility=0.7,
                                falsifiability=0.6,
                                stake_alignment=0.55,
                                evidence_grounding=0.65,
                            ),
                            justification="weaker novelty.",
                        ),
                    ],
                    methodology="Weighted novelty 1.5x feasibility.",
                )
            ]
        )
        ranker = LocalLLMRanker(llm=llm, model="x")  # type: ignore[arg-type]

        refineds = [
            RefinedHypothesis(
                hypothesis_id="h1",
                title="h1",
                statement="s",
                mechanism="m",
                leverages_cells=[],
                addresses_prompts=["a"],
                confidence=0.5,
                revision_notes="r",
                prior_critique_iterations=[0],
            ),
            RefinedHypothesis(
                hypothesis_id="h2",
                title="h2",
                statement="s",
                mechanism="m",
                leverages_cells=[],
                addresses_prompts=["a"],
                confidence=0.8,
                revision_notes="r",
                prior_critique_iterations=[0],
            ),
        ]
        ranking = await ranker.rank(refineds)
        assert [r.hypothesis_id for r in ranking.items] == ["h2", "h1"]
        assert [r.rank for r in ranking.items] == [1, 2]
        assert ranking.methodology.startswith("Weighted novelty")
