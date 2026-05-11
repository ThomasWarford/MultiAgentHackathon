"""PipelineState — the LangGraph state object threaded through every node.

Kept deliberately wide so each stage adds its artifact to a single object;
None marks fields not yet produced. The LLM client mutates `token_spend_usd`
after each call so the cost-ceiling circuit breaker is a state read.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.schemas.critique import CritiqueHistory
from matchmaker.schemas.hypothesis import Hypothesis, RefinedHypothesis
from matchmaker.schemas.matrix import CrossFactorialMatrix
from matchmaker.schemas.prompt import ResearcherPrompt
from matchmaker.schemas.publication import ResearcherProfile
from matchmaker.schemas.ranking import Ranking
from matchmaker.schemas.summary import DimensionalSummary, ResearcherBackground


class PipelineState(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    run_id: str

    profile_a: ResearcherProfile | None = None
    profile_b: ResearcherProfile | None = None

    background_a: ResearcherBackground | None = None
    background_b: ResearcherBackground | None = None

    dimensions_a: list[DimensionalSummary] = Field(default_factory=list)
    dimensions_b: list[DimensionalSummary] = Field(default_factory=list)

    matrix: CrossFactorialMatrix | None = None

    prompt_a: ResearcherPrompt | None = None
    prompt_b: ResearcherPrompt | None = None

    hypotheses: list[Hypothesis] = Field(default_factory=list)

    critique_histories: dict[str, CritiqueHistory] = Field(default_factory=dict)
    refined_hypotheses: list[RefinedHypothesis] = Field(default_factory=list)
    iteration: int = 0

    ranking: Ranking | None = None

    token_spend_usd: float = 0.0
