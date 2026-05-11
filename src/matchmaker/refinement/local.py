"""LocalLLM-backed implementations of the refinement Protocols.

Drop-in default for development before Denario lands. Each class wraps an
OpenAIClient.structured(...) call with the appropriate prompt template
and post-processes the result back into the canonical schema shapes.

These satisfy the Protocols in `protocols.py` — the contract test in
tests/test_refinement_protocols.py asserts it.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from matchmaker.agents.llm import OpenAIClient
from matchmaker.agents.ranking import RankingAgent
from matchmaker.logging import get_logger
from matchmaker.prompts import render
from matchmaker.schemas import (
    Critique,
    CritiqueHistory,
    CritiqueSeverity,
    Dim,
    Hypothesis,
    RefinedHypothesis,
)

log = get_logger(__name__)


# ---------------- Internal LLM response shapes ----------------


class _CritiqueOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    severity: CritiqueSeverity
    strengths: list[str]
    weaknesses: list[str]
    suggested_revisions: list[str]


class _CellRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dim_a: Dim
    dim_b: Dim


class _RefinedOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    statement: str
    mechanism: str
    leverages: list[_CellRef]
    addresses_prompts: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    revision_notes: str


# ---------------- Helpers ----------------


def _format_history(history: CritiqueHistory) -> str:
    if not history.critiques:
        return "(no prior critiques)"
    parts: list[str] = []
    for c in history.critiques:
        parts.append(
            f"### Iteration {c.iteration} — severity={c.severity}\n"
            f"- Strengths: {c.strengths}\n"
            f"- Weaknesses: {c.weaknesses}\n"
            f"- Suggested revisions: {c.suggested_revisions}"
        )
    return "\n\n".join(parts)


def _format_bullets(items: list[str]) -> str:
    if not items:
        return "(none)"
    return "\n  - " + "\n  - ".join(items)


def _format_leverages(cells: list[tuple[Dim, Dim]]) -> str:
    if not cells:
        return "(none)"
    return ", ".join(f"({a}, {b})" for a, b in cells)


def _format_hypothesis(h: RefinedHypothesis | Hypothesis) -> str:
    return (
        f"### [{h.hypothesis_id}] {h.title}\n"
        f"- Statement: {h.statement}\n"
        f"- Mechanism: {h.mechanism}\n"
        f"- Leverages: {_format_leverages(h.leverages_cells)}\n"
        f"- Addresses prompts: {', '.join(h.addresses_prompts) or '(none)'}\n"
        f"- Self-confidence: {h.confidence:.2f}"
    )


# ---------------- Reviewer ----------------


class LocalLLMReviewer:
    reviewer_id: str = "local-openai"

    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model

    async def review(
        self, hypothesis: Hypothesis, history: CritiqueHistory
    ) -> Critique:
        iteration = len(history.critiques)
        prompt = render(
            "reviewer",
            hypothesis_id=hypothesis.hypothesis_id,
            title=hypothesis.title,
            statement=hypothesis.statement,
            mechanism=hypothesis.mechanism,
            confidence=hypothesis.confidence,
            leverages_str=_format_leverages(hypothesis.leverages_cells),
            addresses_str=", ".join(hypothesis.addresses_prompts) or "(none)",
            history_block=_format_history(history),
        )
        log.info(
            "agent.reviewer.start",
            hypothesis_id=hypothesis.hypothesis_id,
            iteration=iteration,
        )
        out = await self._llm.structured(
            model=self._model,
            system="You are a rigorous adversarial reviewer of research hypotheses.",
            user=prompt,
            response_model=_CritiqueOutput,
            temperature=0.4,
            max_tokens=1024,
        )
        critique = Critique(
            hypothesis_id=hypothesis.hypothesis_id,
            iteration=iteration,
            severity=out.severity,
            strengths=out.strengths,
            weaknesses=out.weaknesses,
            suggested_revisions=out.suggested_revisions,
            reviewer_id=self.reviewer_id,
        )
        log.info(
            "agent.reviewer.done",
            hypothesis_id=hypothesis.hypothesis_id,
            iteration=iteration,
            severity=critique.severity,
        )
        return critique


# ---------------- Refiner ----------------


class LocalLLMRefiner:
    refiner_id: str = "local-openai"

    def __init__(self, llm: OpenAIClient, model: str) -> None:
        self._llm = llm
        self._model = model

    async def refine(
        self,
        hypothesis: Hypothesis,
        critique: Critique,
        history: CritiqueHistory,
    ) -> RefinedHypothesis:
        prompt = render(
            "refiner",
            hypothesis_id=hypothesis.hypothesis_id,
            title=hypothesis.title,
            statement=hypothesis.statement,
            mechanism=hypothesis.mechanism,
            confidence=hypothesis.confidence,
            leverages_str=_format_leverages(hypothesis.leverages_cells),
            addresses_str=", ".join(hypothesis.addresses_prompts) or "(none)",
            iteration=critique.iteration,
            severity=critique.severity,
            strengths_block=_format_bullets(critique.strengths),
            weaknesses_block=_format_bullets(critique.weaknesses),
            revisions_block=_format_bullets(critique.suggested_revisions),
            history_block=_format_history(history),
        )
        log.info(
            "agent.refiner.start",
            hypothesis_id=hypothesis.hypothesis_id,
            iteration=critique.iteration,
        )
        out = await self._llm.structured(
            model=self._model,
            system="You produce concrete, evidence-grounded revisions of research hypotheses.",
            user=prompt,
            response_model=_RefinedOutput,
            temperature=0.6,
            max_tokens=2048,
        )
        refined = RefinedHypothesis(
            hypothesis_id=hypothesis.hypothesis_id,
            title=out.title,
            statement=out.statement,
            mechanism=out.mechanism,
            leverages_cells=[(c.dim_a, c.dim_b) for c in out.leverages],
            addresses_prompts=out.addresses_prompts,
            confidence=out.confidence,
            revision_notes=out.revision_notes,
            prior_critique_iterations=[c.iteration for c in history.critiques]
            + [critique.iteration],
        )
        log.info(
            "agent.refiner.done",
            hypothesis_id=hypothesis.hypothesis_id,
            iteration=critique.iteration,
        )
        return refined


# ---------------- Ranker ----------------


class LocalLLMRanker(RankingAgent):
    """Compatibility wrapper for the OpenAI-backed ranking agent."""
