"""Cross-factorial matrix — Stage 4 load-bearing schema.

Self-describing cells in a flat container: every ConnectionCell carries its
own (dim_a, dim_b) labels so JSON artifacts are scannable by humans and the
container survives reshuffling without losing axis identity.
"""

from __future__ import annotations

from itertools import product
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matchmaker.schemas.summary import Dim

ConnectionType = Literal[
    "method_transfer",
    "shared_stake",
    "complementary_gap",
    "analogous_pattern",
    "no_meaningful_link",
]

DIMS: tuple[Dim, ...] = ("methods", "open_questions", "stakes")


class ConnectionCell(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dim_a: Dim
    dim_b: Dim
    items_a: list[str] = Field(description="SummaryItem.item_id values on A's side.")
    items_b: list[str] = Field(description="SummaryItem.item_id values on B's side.")
    connection_type: ConnectionType
    rationale: str = Field(description="3-6 sentences; the substance of the connection.")
    novelty_score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)


class CrossFactorialMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid")

    researcher_a_id: str
    researcher_b_id: str
    cells: list[ConnectionCell] = Field(description="Exactly 9 cells: 3 dims x 3 dims.")

    @model_validator(mode="after")
    def _validate_full_coverage(self) -> "CrossFactorialMatrix":
        seen = {(c.dim_a, c.dim_b) for c in self.cells}
        expected = set(product(DIMS, DIMS))
        if seen != expected:
            missing = expected - seen
            extra = seen - expected
            raise ValueError(
                f"CrossFactorialMatrix must cover all 9 (dim_a, dim_b) pairs exactly once. "
                f"missing={sorted(missing)} extra={sorted(extra)}"
            )
        if len(self.cells) != 9:
            raise ValueError(f"Expected 9 cells, got {len(self.cells)}.")
        return self

    def get(self, dim_a: Dim, dim_b: Dim) -> ConnectionCell:
        for c in self.cells:
            if c.dim_a == dim_a and c.dim_b == dim_b:
                return c
        raise KeyError((dim_a, dim_b))
