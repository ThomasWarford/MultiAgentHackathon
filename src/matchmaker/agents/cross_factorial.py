"""Stage 4 — CrossFactorialAgent.

Runs the 9-cell 3x3 fan-out via asyncio.gather. Each cell is one structured
LLM call producing a per-cell verdict; (dim_a, dim_b) labels are bound by the
caller, so the model only fills the substantive fields.

The constructor of CrossFactorialMatrix enforces exact coverage of the 9
(dim_a, dim_b) pairs — that validator is the canonical shape check.
"""

from __future__ import annotations

import asyncio
from itertools import product

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents.llm import OpenAIClient
from matchmaker.logging import get_logger
from matchmaker.prompts import render
from matchmaker.schemas import (
    DIMS,
    ConnectionCell,
    ConnectionType,
    CrossFactorialMatrix,
    Dim,
    DimensionalSummary,
    ResearcherProfile,
    SummaryItem,
)

log = get_logger(__name__)


class _CellOutput(BaseModel):
    """Internal — dim_a/dim_b are bound by the caller, not the model."""

    model_config = ConfigDict(extra="forbid")

    items_a: list[str] = Field(description="item_ids from researcher A's dimension; may be empty.")
    items_b: list[str] = Field(description="item_ids from researcher B's dimension; may be empty.")
    connection_type: ConnectionType
    rationale: str = Field(description="3-6 sentences.")
    novelty_score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)


def _items_block(items: list[SummaryItem]) -> str:
    if not items:
        return "(no items)"
    return "\n".join(
        f"- [{i.item_id}] **{i.title}** — {i.description}" for i in items
    )


def _summary_by_dim(summaries: list[DimensionalSummary]) -> dict[Dim, DimensionalSummary]:
    out: dict[Dim, DimensionalSummary] = {}
    for s in summaries:
        out[s.dimension] = s
    missing = set(DIMS) - set(out)
    if missing:
        raise ValueError(f"DimensionalSummary set is missing dimensions: {sorted(missing)}")
    return out


class CrossFactorialAgent:
    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model

    async def run(
        self,
        profile_a: ResearcherProfile,
        dims_a: list[DimensionalSummary],
        profile_b: ResearcherProfile,
        dims_b: list[DimensionalSummary],
    ) -> CrossFactorialMatrix:
        by_dim_a = _summary_by_dim(dims_a)
        by_dim_b = _summary_by_dim(dims_b)

        log.info(
            "agent.cross_factorial.start",
            researcher_a=profile_a.researcher_id,
            researcher_b=profile_b.researcher_id,
        )

        coords: list[tuple[Dim, Dim]] = list(product(DIMS, DIMS))
        coros = [
            self._one_cell(
                dim_a=da,
                dim_b=db,
                display_a=profile_a.display_name,
                display_b=profile_b.display_name,
                summary_a=by_dim_a[da],
                summary_b=by_dim_b[db],
            )
            for da, db in coords
        ]
        cell_outputs = await asyncio.gather(*coros)

        cells = [
            ConnectionCell(
                dim_a=da,
                dim_b=db,
                items_a=out.items_a,
                items_b=out.items_b,
                connection_type=out.connection_type,
                rationale=out.rationale,
                novelty_score=out.novelty_score,
                confidence=out.confidence,
            )
            for (da, db), out in zip(coords, cell_outputs, strict=True)
        ]
        matrix = CrossFactorialMatrix(
            researcher_a_id=profile_a.researcher_id,
            researcher_b_id=profile_b.researcher_id,
            cells=cells,
        )
        log.info(
            "agent.cross_factorial.done",
            researcher_a=profile_a.researcher_id,
            researcher_b=profile_b.researcher_id,
            n_cells=len(matrix.cells),
            n_no_link=sum(1 for c in matrix.cells if c.connection_type == "no_meaningful_link"),
        )
        return matrix

    async def _one_cell(
        self,
        *,
        dim_a: Dim,
        dim_b: Dim,
        display_a: str,
        display_b: str,
        summary_a: DimensionalSummary,
        summary_b: DimensionalSummary,
    ) -> _CellOutput:
        prompt = render(
            "cross_factorial",
            display_a=display_a,
            display_b=display_b,
            dim_a=dim_a,
            dim_b=dim_b,
            items_a_block=_items_block(summary_a.items),
            items_b_block=_items_block(summary_b.items),
        )
        return await self._llm.structured(
            model=self._model,
            system=(
                "You identify non-obvious cross-disciplinary connections between "
                "research dimensions. Prefer null results over confabulation."
            ),
            user=prompt,
            response_model=_CellOutput,
            temperature=1.0,
            max_tokens=4096,
        )
