"""OpenAI-backed final ranking agent."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents.llm import OpenAIClient
from matchmaker.logging import get_logger
from matchmaker.prompts import render
from matchmaker.schemas import Dim, RankedHypothesis, Ranking, RefinedHypothesis

log = get_logger(__name__)


class _DimensionScoresOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    novelty: float = Field(ge=0.0, le=1.0)
    feasibility: float = Field(ge=0.0, le=1.0)
    falsifiability: float = Field(ge=0.0, le=1.0)
    stake_alignment: float = Field(ge=0.0, le=1.0)
    evidence_grounding: float = Field(ge=0.0, le=1.0)


class _RankedItemOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    rank: int = Field(ge=1)
    composite_score: float = Field(ge=0.0, le=1.0)
    dimension_scores: _DimensionScoresOutput
    justification: str


class _RankingOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[_RankedItemOutput]
    methodology: str


def _format_leverages(cells: list[tuple[Dim, Dim]]) -> str:
    if not cells:
        return "(none)"
    return ", ".join(f"({a}, {b})" for a, b in cells)


def _format_hypothesis(h: RefinedHypothesis) -> str:
    return (
        f"### [{h.hypothesis_id}] {h.title}\n"
        f"- Statement: {h.statement}\n"
        f"- Mechanism: {h.mechanism}\n"
        f"- Leverages: {_format_leverages(h.leverages_cells)}\n"
        f"- Addresses prompts: {', '.join(h.addresses_prompts) or '(none)'}\n"
        f"- Self-confidence: {h.confidence:.2f}"
    )


class RankingAgent:
    ranker_id: str = "local-openai"

    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model

    async def rank(self, hypotheses: list[RefinedHypothesis]) -> Ranking:
        if not hypotheses:
            return Ranking(items=[], methodology="No hypotheses to rank.", ranker_id=self.ranker_id)

        block = "\n\n".join(_format_hypothesis(h) for h in hypotheses)
        prompt = render("ranker", hypotheses_block=block)
        log.info("agent.ranking.start", n_hypotheses=len(hypotheses))
        out = await self._llm.structured(
            model=self._model,
            system="You are a ranking agent that scores research hypotheses by rigor, novelty, and feasibility.",
            user=prompt,
            response_model=_RankingOutput,
            temperature=0.2,
            max_tokens=3072,
        )
        items = [
            RankedHypothesis(
                hypothesis_id=item.hypothesis_id,
                rank=item.rank,
                composite_score=item.composite_score,
                dimension_scores=item.dimension_scores.model_dump(),
                justification=item.justification,
            )
            for item in out.items
        ]
        log.info("agent.ranking.done", n_ranked=len(items))
        return Ranking(items=items, methodology=out.methodology, ranker_id=self.ranker_id)
