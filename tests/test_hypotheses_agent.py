"""HypothesesAgent unit tests with a mocked LLM."""

from __future__ import annotations

from itertools import product
from typing import Any

from matchmaker.agents.hypotheses import (
    HypothesesAgent,
    _CellRef,
    _HypothesesOutput,
    _HypothesisDraft,
)
from matchmaker.schemas import (
    DIMS,
    ConnectionCell,
    CrossFactorialMatrix,
    Hypothesis,
    ResearcherBackground,
    ResearcherPrompt,
)


def _full_matrix() -> CrossFactorialMatrix:
    cells = []
    for a, b in product(DIMS, DIMS):
        cells.append(
            ConnectionCell(
                dim_a=a,
                dim_b=b,
                items_a=["x"],
                items_b=["y"],
                connection_type="method_transfer" if (a, b) != ("stakes", "stakes") else "shared_stake",
                rationale="r",
                novelty_score=0.5,
                confidence=0.5,
            )
        )
    return CrossFactorialMatrix(
        researcher_a_id="alice", researcher_b_id="bob", cells=cells
    )


class _FakeLLM:
    def __init__(self, response: _HypothesesOutput) -> None:
        self._response = response
        self.captured: list[dict[str, Any]] = []

    async def structured(self, **kwargs: Any) -> _HypothesesOutput:
        self.captured.append(kwargs)
        return self._response


async def test_converts_cell_refs_to_tuples() -> None:
    response = _HypothesesOutput(
        hypotheses=[
            _HypothesisDraft(
                hypothesis_id="h1",
                title="A Hypothesis",
                statement="A is true.",
                mechanism="Do the thing.",
                leverages=[
                    _CellRef(dim_a="methods", dim_b="open_questions"),
                    _CellRef(dim_a="stakes", dim_b="stakes"),
                ],
                addresses_prompts=["alice"],
                confidence=0.8,
            )
        ]
    )
    llm = _FakeLLM(response)
    agent = HypothesesAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

    out = await agent.run(
        background_a=ResearcherBackground(researcher_id="alice", narrative="A bg", keywords=[]),
        background_b=ResearcherBackground(researcher_id="bob", narrative="B bg", keywords=[]),
        prompt_a=ResearcherPrompt(researcher_id="alice", current_focus="x"),
        prompt_b=ResearcherPrompt(researcher_id="bob", current_focus="y"),
        matrix=_full_matrix(),
        display_a="Alice",
        display_b="Bob",
    )

    assert len(out) == 1
    assert isinstance(out[0], Hypothesis)
    assert out[0].leverages_cells == [
        ("methods", "open_questions"),
        ("stakes", "stakes"),
    ]


async def test_prompt_includes_matrix_cells_and_blockers() -> None:
    response = _HypothesesOutput(hypotheses=[])
    llm = _FakeLLM(response)
    agent = HypothesesAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

    await agent.run(
        background_a=ResearcherBackground(
            researcher_id="alice", narrative="A bg detail", keywords=[]
        ),
        background_b=ResearcherBackground(
            researcher_id="bob", narrative="B bg detail", keywords=[]
        ),
        prompt_a=ResearcherPrompt(
            researcher_id="alice",
            current_focus="alice's focus",
            blockers=["alice-blocker-1"],
        ),
        prompt_b=ResearcherPrompt(
            researcher_id="bob",
            current_focus="bob's focus",
            blockers=["bob-blocker-1"],
        ),
        matrix=_full_matrix(),
        display_a="Alice",
        display_b="Bob",
    )
    rendered = llm.captured[0]["user"]
    assert "alice's focus" in rendered
    assert "alice-blocker-1" in rendered
    assert "[methods × stakes]" in rendered
    assert "shared_stake" in rendered
