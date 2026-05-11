"""Backend selection for the refinement stack.

The factory is the one place the orchestrator touches concrete classes; every
other component depends only on the Protocols. Adding a new backend means:
add a branch here + a module that satisfies the Protocols.
"""

from __future__ import annotations

from matchmaker.agents.ranking import RankingAgent
from matchmaker.agents.llm import OpenAIClient
from matchmaker.config import Settings
from matchmaker.refinement.denario import DenarioRanker, DenarioRefiner, DenarioReviewer
from matchmaker.refinement.local import LocalLLMRefiner, LocalLLMReviewer
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


def build_refinement_stack(
    settings: Settings,
    *,
    llm: OpenAIClient | None = None,
) -> RefinementStack:
    """Build the refinement triple matching `settings.refinement_backend`.

    `llm` is required when backend == "local" (LocalLLM* implementations need
    a shared OpenAIClient for cost tracking). It is ignored otherwise.
    """
    backend = settings.refinement_backend
    if backend == "mock":
        return RefinementStack(MockReviewer(), MockRefiner(), MockRanker())
    if backend == "local":
        if llm is None:
            raise ValueError(
                "refinement_backend='local' requires an OpenAIClient via the `llm` arg."
            )
        return RefinementStack(
            LocalLLMReviewer(llm, settings.model_refinement),
            LocalLLMRefiner(llm, settings.model_refinement),
            RankingAgent(llm, settings.model_ranking),
        )
    if backend == "denario":
        return RefinementStack(
            DenarioReviewer(settings.denario_base_url, settings.denario_api_key),
            DenarioRefiner(settings.denario_base_url, settings.denario_api_key),
            DenarioRanker(settings.denario_base_url, settings.denario_api_key),
        )
    raise ValueError(f"Unknown refinement backend: {backend!r}")
