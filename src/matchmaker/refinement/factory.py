"""Backend selection for the refinement stack.

The factory is the one place the orchestrator touches concrete classes; every
other component depends only on the Protocols. Adding a new backend means:
add a branch here + a module that satisfies the Protocols.
"""

from __future__ import annotations

from matchmaker.config import Settings
from matchmaker.refinement.denario import DenarioRanker, DenarioRefiner, DenarioReviewer
from matchmaker.refinement.mocks import MockRanker, MockRefiner, MockReviewer
from matchmaker.refinement.protocols import (
    RankerProtocol,
    RefinerProtocol,
    ReviewerProtocol,
)


class RefinementStack:
    def __init__(
        self,
        reviewer: ReviewerProtocol,
        refiner: RefinerProtocol,
        ranker: RankerProtocol,
    ) -> None:
        self.reviewer = reviewer
        self.refiner = refiner
        self.ranker = ranker


def build_refinement_stack(settings: Settings) -> RefinementStack:
    backend = settings.refinement_backend
    if backend == "mock":
        return RefinementStack(MockReviewer(), MockRefiner(), MockRanker())
    if backend == "denario":
        return RefinementStack(
            DenarioReviewer(settings.denario_base_url, settings.denario_api_key),
            DenarioRefiner(settings.denario_base_url, settings.denario_api_key),
            DenarioRanker(settings.denario_base_url, settings.denario_api_key),
        )
    if backend == "local":
        raise NotImplementedError(
            "LocalLLM refinement backend lands in step 10; use 'mock' until then."
        )
    raise ValueError(f"Unknown refinement backend: {backend!r}")
