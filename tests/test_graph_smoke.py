"""End-to-end DAG smoke test.

Builds the full LangGraph pipeline against the real papers/ corpus, mocks
the OpenAI client so no network calls happen, runs the graph, and asserts
every stage emitted a well-formed artifact.

The refinement backend is "mock" — that avoids exercising the LocalLLM
review/refine/rank path (the unit tests in test_refinement_local.py cover
that). What this test exercises is the orchestration and artifact-writing
plumbing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel

from matchmaker.agents.background import _BackgroundOutput
from matchmaker.agents.cross_factorial import _CellOutput
from matchmaker.agents.extraction import _ItemsOutput
from matchmaker.agents.hypotheses import (
    _CellRef,
    _HypothesesOutput,
    _HypothesisDraft,
)
from matchmaker.agents.llm import OpenAIClient
from matchmaker.config import Settings
from matchmaker.ingestion import LocalCorpusSource
from matchmaker.orchestrator import GraphContext, build_graph
from matchmaker.refinement import build_refinement_stack
from matchmaker.schemas import (
    CrossFactorialMatrix,
    DimensionalSummary,
    PipelineState,
    Ranking,
    SummaryItem,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "papers"


pytestmark = pytest.mark.skipif(
    not PAPERS_DIR.exists(), reason="papers/ corpus not present"
)


class _MockedOpenAIClient(OpenAIClient):
    """Returns canned response_model instances; never touches the network."""

    def __init__(self) -> None:  # noqa: D401 — intentional override
        # Skip parent __init__'s real-key check; we don't have an API key in CI.
        self._client = None  # type: ignore[assignment]
        self._ceiling = 100.0
        from matchmaker.agents.llm import TokenSpend

        self.spend = TokenSpend()

    async def structured(  # type: ignore[override]
        self,
        *,
        model: str,
        system: str,
        user: str,
        response_model: type[BaseModel],
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ) -> BaseModel:
        name = response_model.__name__
        self.spend.add(model, input_tokens=100, output_tokens=80)

        if name == "_BackgroundOutput":
            return _BackgroundOutput(
                narrative="A canned background narrative.",
                keywords=["k1", "k2", "k3"],
            )
        if name == "_ItemsOutput":
            return _ItemsOutput(
                items=[
                    SummaryItem(
                        item_id="i1",
                        title="An item",
                        description="A description.",
                        evidence=[],
                    ),
                    SummaryItem(
                        item_id="i2",
                        title="Another item",
                        description="A description.",
                        evidence=[],
                    ),
                ]
            )
        if name == "_CellOutput":
            return _CellOutput(
                items_a=["i1"],
                items_b=["i1"],
                connection_type="method_transfer",
                rationale="A canned cell rationale.",
                novelty_score=0.5,
                confidence=0.6,
            )
        if name == "_HypothesesOutput":
            return _HypothesesOutput(
                hypotheses=[
                    _HypothesisDraft(
                        hypothesis_id=f"h{i}",
                        title=f"Hypothesis {i}",
                        statement="A claim.",
                        mechanism="A mechanism.",
                        leverages=[_CellRef(dim_a="methods", dim_b="stakes")],
                        addresses_prompts=["csanyi", "pellegrini"],
                        confidence=0.5 + 0.1 * i,
                    )
                    for i in range(3)
                ]
            )

        raise AssertionError(f"Unmocked response_model: {name}")


async def test_end_to_end_pipeline(tmp_path: Path) -> None:
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "csanyi.md").write_text(
        "## Current focus\nMLIPs for liquid water at coupled-cluster accuracy.\n"
        "## Blockers\n- DFT noise\n",
        encoding="utf-8",
    )
    (prompts_dir / "pellegrini.md").write_text(
        "## Current focus\nFire-driven SOC dynamics in drylands.\n"
        "## Blockers\n- Multi-decadal data scarcity\n",
        encoding="utf-8",
    )

    outputs_dir = tmp_path / "outputs"
    settings = Settings(refinement_backend="mock", max_iterations=2)
    llm = _MockedOpenAIClient()
    stack = build_refinement_stack(settings, llm=llm)
    source = LocalCorpusSource(PAPERS_DIR)

    ctx = GraphContext(
        settings=settings,
        llm=llm,
        source=source,
        stack=stack,
        researcher_a_id="csanyi",
        researcher_b_id="pellegrini",
        prompts_dir=prompts_dir,
    )
    graph = build_graph(ctx)

    initial = PipelineState(run_id="smoke")
    final_dict = await graph.ainvoke(
        initial.model_dump(),
        config={"recursion_limit": 50},
    )
    final = PipelineState.model_validate(final_dict)

    # Shape invariants
    assert final.profile_a and final.profile_b
    assert final.background_a and final.background_b
    assert len(final.dimensions_a) == 3 and len(final.dimensions_b) == 3
    assert isinstance(final.matrix, CrossFactorialMatrix)
    assert len(final.matrix.cells) == 9
    assert final.prompt_a and final.prompt_b
    assert len(final.hypotheses) == 3
    assert len(final.refined_hypotheses) == 3
    assert isinstance(final.ranking, Ranking)
    assert {r.hypothesis_id for r in final.ranking.items} == {
        h.hypothesis_id for h in final.refined_hypotheses
    }

    # Mock reviewer accepts on iter 1, so each hypothesis went through 1 refine.
    assert final.iteration == 2  # iteration 0 (suggest) + iteration 1 (accept) = 2 critiques

    # Artifact writes
    from matchmaker.cli import _write_all_artifacts

    final.token_spend_usd = llm.spend.usd
    _write_all_artifacts(outputs_dir, "smoke", final)

    for stage in [
        "01_publications",
        "02_backgrounds",
        "03_dimensional",
        "04_matrix",
        "05_hypotheses",
        "06_critiques",
        "07_refined",
        "08_ranking",
    ]:
        stage_dir = outputs_dir / stage
        files = list(stage_dir.glob("*.json"))
        assert len(files) == 1, f"missing artifact for {stage}"
        body = json.loads(files[0].read_text(encoding="utf-8"))
        assert body["stage"] == stage
        assert body["run_id"] == "smoke"

    # Matrix artifact must round-trip back into a CrossFactorialMatrix.
    matrix_body = json.loads(
        (outputs_dir / "04_matrix").glob("*.json").__next__().read_text(encoding="utf-8")
    )
    rebuilt = CrossFactorialMatrix.model_validate(matrix_body["payload"])
    assert len(rebuilt.cells) == 9
