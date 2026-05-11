"""Mock refinement backend — deterministic outputs for development and tests.

Per CLAUDE.md: "Use mock functions for these stages during initial development."
These let the orchestrator run end-to-end before LocalLLMReviewer (Claude-backed)
lands in a later step, and before Denario endpoints arrive.

Behavior:
- MockReviewer accepts on iteration >= 1, suggests on iteration 0.
- MockRefiner trivially echoes the hypothesis with a revision note.
- MockRanker sorts by descending hypothesis.confidence.
"""

from __future__ import annotations

from matchmaker.schemas import (
    Critique,
    CritiqueHistory,
    Hypothesis,
    RankedHypothesis,
    Ranking,
    RefinedHypothesis,
)


class MockReviewer:
    reviewer_id: str = "mock-v0"

    async def review(self, hypothesis: Hypothesis, history: CritiqueHistory) -> Critique:
        iteration = len(history.critiques)
        if iteration >= 1:
            return Critique(
                hypothesis_id=hypothesis.hypothesis_id,
                iteration=iteration,
                severity="accept",
                strengths=["Mock: accepted on second pass."],
                weaknesses=[],
                suggested_revisions=[],
                reviewer_id=self.reviewer_id,
            )
        return Critique(
            hypothesis_id=hypothesis.hypothesis_id,
            iteration=iteration,
            severity="suggest",
            strengths=["Mock: clear statement."],
            weaknesses=["Mock: mechanism could be tighter."],
            suggested_revisions=["Mock: name a specific experiment."],
            reviewer_id=self.reviewer_id,
        )


class MockRefiner:
    refiner_id: str = "mock-v0"

    async def refine(
        self,
        hypothesis: Hypothesis,
        critique: Critique,
        history: CritiqueHistory,
    ) -> RefinedHypothesis:
        return RefinedHypothesis(
            hypothesis_id=hypothesis.hypothesis_id,
            title=hypothesis.title,
            statement=hypothesis.statement,
            mechanism=hypothesis.mechanism + " [mock-refined]",
            leverages_cells=hypothesis.leverages_cells,
            addresses_prompts=hypothesis.addresses_prompts,
            confidence=hypothesis.confidence,
            revision_notes=f"Mock-applied {len(critique.suggested_revisions)} suggestions.",
            prior_critique_iterations=[c.iteration for c in history.critiques],
        )


class MockRanker:
    ranker_id: str = "mock-v0"

    async def rank(self, hypotheses: list[RefinedHypothesis]) -> Ranking:
        ordered = sorted(hypotheses, key=lambda h: h.confidence, reverse=True)
        items = [
            RankedHypothesis(
                hypothesis_id=h.hypothesis_id,
                rank=i + 1,
                composite_score=h.confidence,
                dimension_scores={"confidence": h.confidence},
                justification="Mock ranker: sorted by self-reported confidence.",
            )
            for i, h in enumerate(ordered)
        ]
        return Ranking(
            items=items,
            methodology="Mock: descending hypothesis.confidence.",
            ranker_id=self.ranker_id,
        )
