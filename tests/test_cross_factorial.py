"""Cross-factorial agent shape and coverage tests."""

from __future__ import annotations

from itertools import product
from typing import Any

import pytest

from matchmaker.agents.cross_factorial import CrossFactorialAgent, _CellOutput
from matchmaker.schemas import (
    DIMS,
    Dim,
    DimensionalSummary,
    Publication,
    ResearcherProfile,
    SummaryItem,
)


def _profile(rid: str) -> ResearcherProfile:
    return ResearcherProfile(
        researcher_id=rid,
        display_name=rid.title(),
        publications=[
            Publication(
                id=f"{rid}_1",
                title=f"{rid.title()} Paper 1",
                source="local",
                source_id=f"{rid}_1.md",
                full_text_md="content",
            ),
        ],
    )


def _summary(rid: str, dim: Dim) -> DimensionalSummary:
    return DimensionalSummary(
        researcher_id=rid,
        dimension=dim,
        items=[
            SummaryItem(
                item_id=f"{rid}-{dim}-1",
                title=f"{dim} item",
                description="desc",
                evidence=[f"{rid}_1"],
            )
        ],
    )


class _FakeLLM:
    """Tracks every call's (dim_a, dim_b) so we can verify exact coverage."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def structured(self, **kwargs: Any) -> _CellOutput:
        self.calls.append(kwargs)
        # Echo back a benign cell. dim labels live in the prompt; the model
        # itself never sees them as inputs to its output schema.
        return _CellOutput(
            items_a=["a"],
            items_b=["b"],
            connection_type="method_transfer",
            rationale="A connects to B because of x.",
            novelty_score=0.5,
            confidence=0.6,
        )


class TestCrossFactorialAgent:
    async def test_produces_9_cells_with_full_coverage(self) -> None:
        llm = _FakeLLM()
        agent = CrossFactorialAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

        profile_a = _profile("alice")
        profile_b = _profile("bob")
        dims_a = [_summary("alice", d) for d in DIMS]
        dims_b = [_summary("bob", d) for d in DIMS]

        matrix = await agent.run(profile_a, dims_a, profile_b, dims_b)

        assert matrix.researcher_a_id == "alice"
        assert matrix.researcher_b_id == "bob"
        assert len(matrix.cells) == 9
        observed = {(c.dim_a, c.dim_b) for c in matrix.cells}
        assert observed == set(product(DIMS, DIMS))

        # 9 LLM calls, no more, no less.
        assert len(llm.calls) == 9

    async def test_raises_if_summaries_missing_a_dimension(self) -> None:
        llm = _FakeLLM()
        agent = CrossFactorialAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

        profile_a = _profile("alice")
        profile_b = _profile("bob")
        # Drop one dimension on side A.
        dims_a = [_summary("alice", d) for d in DIMS if d != "stakes"]
        dims_b = [_summary("bob", d) for d in DIMS]

        with pytest.raises(ValueError, match="missing dimensions"):
            await agent.run(profile_a, dims_a, profile_b, dims_b)

    async def test_get_returns_per_coordinate_cell(self) -> None:
        llm = _FakeLLM()
        agent = CrossFactorialAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

        matrix = await agent.run(
            _profile("alice"),
            [_summary("alice", d) for d in DIMS],
            _profile("bob"),
            [_summary("bob", d) for d in DIMS],
        )
        for da, db in product(DIMS, DIMS):
            cell = matrix.get(da, db)
            assert cell.dim_a == da and cell.dim_b == db


class TestPromptRendering:
    async def test_prompt_includes_both_dims_and_display_names(self) -> None:
        llm = _FakeLLM()
        agent = CrossFactorialAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

        await agent.run(
            _profile("alice"),
            [_summary("alice", d) for d in DIMS],
            _profile("bob"),
            [_summary("bob", d) for d in DIMS],
        )
        # Find the methods x stakes call and verify the rendered prompt has both labels.
        for call in llm.calls:
            user = call["user"]
            if "Dimension: **methods**" in user and "Dimension: **stakes**" in user:
                assert "Alice" in user and "Bob" in user
                assert "alice-methods-1" in user
                assert "bob-stakes-1" in user
                return
        pytest.fail("Did not find a (methods, stakes) prompt rendering.")
