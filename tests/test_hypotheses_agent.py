"""HypothesesAgent unit tests with a mocked LLM."""

from __future__ import annotations

from itertools import product
from typing import Any

from matchmaker.agents.hypotheses import (
    HypothesisFilterAgent,
    HypothesesAgent,
    _CellRef,
    _DuplicateGroup,
    _HypothesisFilterOutput,
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
    def __init__(self, *responses: Any) -> None:
        self._responses = list(responses)
        self.captured: list[dict[str, Any]] = []

    async def structured(self, **kwargs: Any) -> Any:
        self.captured.append(kwargs)
        return self._responses.pop(0)


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


async def test_hypothesis_filter_agent_drops_duplicate_ids_without_llm_call() -> None:
    first = Hypothesis(
        hypothesis_id="same-id",
        title="First hypothesis",
        statement="A first falsifiable claim.",
        mechanism="Run the first collaboration.",
        confidence=0.7,
    )
    duplicate = Hypothesis(
        hypothesis_id="same-id",
        title="Different wording",
        statement="A different claim.",
        mechanism="Run a different collaboration.",
        confidence=0.8,
    )
    llm = _FakeLLM()
    agent = HypothesisFilterAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

    assert await agent.run([first, duplicate]) == [first]
    assert llm.captured == []


async def test_hypothesis_filter_agent_uses_llm_to_drop_semantic_duplicates() -> None:
    first = Hypothesis(
        hypothesis_id="h1",
        title="ML force fields predict fire carbon flux",
        statement="Machine-learned force fields can predict fire-driven carbon flux from soil molecular structure.",
        mechanism="Train force fields on soil organic matter structures and compare predictions with fire treatment data.",
        confidence=0.7,
    )
    duplicate = Hypothesis(
        hypothesis_id="h2",
        title="ML force fields predict fire carbon flux",
        statement="Machine learned force fields can predict fire driven carbon flux from soil molecular structure.",
        mechanism="Train force fields on soil organic matter structures and compare predictions with fire treatment data.",
        confidence=0.8,
    )
    distinct = Hypothesis(
        hypothesis_id="h3",
        title="Remote sensing benchmarks combustion models",
        statement="Satellite fire histories can benchmark uncertainty in ecosystem combustion models.",
        mechanism="Compare remote-sensing burn histories with modelled carbon losses across sites.",
        confidence=0.6,
    )
    filter_response = _HypothesisFilterOutput(
        keep_hypothesis_ids=["h1", "h3"],
        duplicate_groups=[
            _DuplicateGroup(
                keep_hypothesis_id="h1",
                duplicate_hypothesis_ids=["h2"],
                rationale="Both test the same claim using the same soil simulation and fire-treatment mechanism.",
            )
        ],
    )
    llm = _FakeLLM(filter_response)
    agent = HypothesisFilterAgent(llm=llm, model="gpt-4o-mini")  # type: ignore[arg-type]

    assert await agent.run([first, duplicate, distinct]) == [first, distinct]
    assert llm.captured[0]["response_model"] is _HypothesisFilterOutput
    assert "semantic duplicates" in llm.captured[0]["system"]
