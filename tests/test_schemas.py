"""Schema invariants: round-trip, extra='forbid', matrix coverage validator."""

from __future__ import annotations

from itertools import product

import pytest
from pydantic import ValidationError

from matchmaker.schemas import (
    DIMS,
    ConnectionCell,
    CrossFactorialMatrix,
    Critique,
    CritiqueHistory,
    DimensionalSummary,
    Hypothesis,
    Publication,
    ResearcherProfile,
    SummaryItem,
)


def _cell(dim_a, dim_b) -> ConnectionCell:
    return ConnectionCell(
        dim_a=dim_a,
        dim_b=dim_b,
        items_a=["a1"],
        items_b=["b1"],
        connection_type="method_transfer",
        rationale="x" * 20,
        novelty_score=0.5,
        confidence=0.7,
    )


def _full_matrix() -> CrossFactorialMatrix:
    return CrossFactorialMatrix(
        researcher_a_id="a",
        researcher_b_id="b",
        cells=[_cell(a, b) for a, b in product(DIMS, DIMS)],
    )


class TestExtraForbid:
    def test_publication_rejects_unknown_field(self) -> None:
        with pytest.raises(ValidationError):
            Publication(
                id="x",
                title="t",
                source="local",
                source_id="x.md",
                bogus_field=1,  # type: ignore[call-arg]
            )

    def test_summary_item_rejects_unknown_field(self) -> None:
        with pytest.raises(ValidationError):
            SummaryItem(
                item_id="i1",
                title="t",
                description="d",
                bogus=True,  # type: ignore[call-arg]
            )


class TestRoundTrip:
    def test_researcher_profile_json_round_trip(self) -> None:
        pub = Publication(
            id="p1",
            title="A paper",
            source="local",
            source_id="p1.md",
        )
        profile = ResearcherProfile(
            researcher_id="csanyi",
            display_name="Gabor Csanyi",
            publications=[pub],
        )
        data = profile.model_dump_json()
        restored = ResearcherProfile.model_validate_json(data)
        assert restored == profile

    def test_critique_history_round_trip(self) -> None:
        history = CritiqueHistory(
            hypothesis_id="h1",
            critiques=[
                Critique(
                    hypothesis_id="h1",
                    iteration=0,
                    severity="suggest",
                    reviewer_id="local-claude",
                ),
                Critique(
                    hypothesis_id="h1",
                    iteration=1,
                    severity="accept",
                    reviewer_id="local-claude",
                ),
            ],
        )
        assert history.latest() is not None
        assert history.latest().severity == "accept"
        restored = CritiqueHistory.model_validate_json(history.model_dump_json())
        assert restored == history

    def test_dimensional_summary_round_trip(self) -> None:
        ds = DimensionalSummary(
            researcher_id="csanyi",
            dimension="methods",
            items=[
                SummaryItem(
                    item_id="m1",
                    title="Machine-learned interatomic potentials",
                    description="MLIPs for condensed-phase molecular simulation.",
                    evidence=["p1"],
                ),
            ],
        )
        assert ds == DimensionalSummary.model_validate_json(ds.model_dump_json())


class TestCrossFactorialMatrix:
    def test_full_9_cell_matrix_validates(self) -> None:
        m = _full_matrix()
        assert len(m.cells) == 9

    def test_missing_cell_rejected(self) -> None:
        cells = [_cell(a, b) for a, b in product(DIMS, DIMS) if (a, b) != ("methods", "stakes")]
        with pytest.raises(ValidationError):
            CrossFactorialMatrix(researcher_a_id="a", researcher_b_id="b", cells=cells)

    def test_duplicate_cell_rejected(self) -> None:
        cells = [_cell(a, b) for a, b in product(DIMS, DIMS)]
        cells.append(_cell("methods", "methods"))
        with pytest.raises(ValidationError):
            CrossFactorialMatrix(researcher_a_id="a", researcher_b_id="b", cells=cells)

    def test_get_returns_correct_cell(self) -> None:
        m = _full_matrix()
        cell = m.get("methods", "stakes")
        assert cell.dim_a == "methods" and cell.dim_b == "stakes"

    def test_get_raises_keyerror_on_invalid_combo(self) -> None:
        cells = [_cell(a, b) for a, b in product(DIMS, DIMS) if (a, b) != ("stakes", "stakes")]
        # Can't even construct the matrix without all 9, so synthesize a partial one
        # by skipping the validator via model_construct.
        partial = CrossFactorialMatrix.model_construct(
            researcher_a_id="a", researcher_b_id="b", cells=cells
        )
        with pytest.raises(KeyError):
            partial.get("stakes", "stakes")


class TestHypothesisCells:
    def test_hypothesis_leverages_cell_tuples_round_trip(self) -> None:
        h = Hypothesis(
            hypothesis_id="h1",
            title="t",
            statement="claim",
            mechanism="how",
            leverages_cells=[("methods", "open_questions"), ("stakes", "stakes")],
            addresses_prompts=["a", "b"],
            confidence=0.8,
        )
        restored = Hypothesis.model_validate_json(h.model_dump_json())
        assert restored.leverages_cells == [
            ("methods", "open_questions"),
            ("stakes", "stakes"),
        ]
