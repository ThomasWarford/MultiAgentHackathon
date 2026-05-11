"""Shared OpenAI client.

Every Stage 1-6 agent calls `OpenAIClient.structured(...)` with a Pydantic
response_model. The client:
- forces structured output via OpenAI's native structured outputs
  (`chat.completions.parse` with response_format=BaseModel),
- updates a shared TokenSpend tracker after each call,
- raises CostCeilingExceeded before issuing a call that would push spend over
  the configured ceiling, so a runaway refinement loop terminates predictably,
- logs a structured event at every call boundary (CLAUDE.md handoff rule).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from matchmaker.logging import get_logger

T = TypeVar("T", bound=BaseModel)

log = get_logger(__name__)


# USD per 1M tokens (OpenAI public pricing; tune as their pricing evolves).
# Tiers are roughly: nano/mini = cheap (testing), full = expensive (production).
MODEL_PRICING: dict[str, tuple[float, float]] = {
    # Cheap tier — use for development, testing, bulk fan-out (e.g. the 9-cell
    # cross-factorial matrix).
    "gpt-4o-mini": (0.15, 0.60),
    # Current default across all stages. Pricing is a placeholder — confirm
    # against OpenAI's published rates before relying on cost-ceiling math.
    "gpt-5.5": (0.15, 0.60),
    # Mid/high tier — use for the synthesis & refinement stages once you trust
    # the pipeline and want better reasoning quality.
    "gpt-4o": (2.50, 10.00),
    # Reasoning tier — slow and expensive; only worth it for final ranking
    # against a small candidate set.
    "o1-mini": (3.00, 12.00),
    "o1": (15.00, 60.00),
}

# Models that only support the default temperature (1.0).
_FIXED_TEMPERATURE_MODELS: set[str] = {"gpt-5.5", "o1-mini", "o1"}


class CostCeilingExceeded(RuntimeError):
    """Raised when projected or actual spend crosses the configured ceiling."""


@dataclass
class TokenSpend:
    usd: float = 0.0
    calls: int = 0
    by_model: dict[str, float] = field(default_factory=dict)

    def add(self, model: str, input_tokens: int, output_tokens: int) -> float:
        rates = MODEL_PRICING.get(model, (5.0, 25.0))  # fallback ~mid-tier
        delta = (input_tokens * rates[0] + output_tokens * rates[1]) / 1_000_000.0
        self.usd += delta
        self.calls += 1
        self.by_model[model] = self.by_model.get(model, 0.0) + delta
        return delta


class OpenAIClient:
    def __init__(
        self,
        *,
        api_key: str,
        cost_ceiling_usd: float,
        spend: TokenSpend | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is empty; set it in .env.")
        self._client = AsyncOpenAI(api_key=api_key)
        self._ceiling = cost_ceiling_usd
        self.spend = spend or TokenSpend()

    async def structured(
        self,
        *,
        model: str,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 1.0,
        max_tokens: int = 4096,
    ) -> T:
        if self.spend.usd >= self._ceiling:
            raise CostCeilingExceeded(
                f"Spend ${self.spend.usd:.4f} >= ceiling ${self._ceiling:.4f}; "
                f"refusing further LLM calls."
            )

        response_name = response_model.__name__

        # Some models (e.g. gpt-5.5, o1) only support temperature=1.
        if model in _FIXED_TEMPERATURE_MODELS and temperature != 1.0:
            log.info(
                "llm.temperature.clamped",
                model=model,
                requested=temperature,
                effective=1.0,
            )
            temperature = 1.0

        log.info(
            "llm.call.start",
            model=model,
            response_model=response_name,
            spend_usd=round(self.spend.usd, 4),
            temperature=temperature,
        )

        response = await self._client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format=response_model,
            temperature=temperature,
            max_completion_tokens=max_tokens,
        )

        usage = response.usage
        input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
        output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0
        delta = self.spend.add(model, input_tokens, output_tokens)

        choice = response.choices[0]
        message = choice.message

        if getattr(message, "refusal", None):
            raise RuntimeError(
                f"OpenAI refused to produce {response_name!r}: {message.refusal}"
            )

        parsed = message.parsed
        if parsed is None:
            raise RuntimeError(
                f"OpenAI returned no parsed object for {response_name!r}; "
                f"finish_reason={choice.finish_reason!r}."
            )

        log.info(
            "llm.call.done",
            model=model,
            response_model=response_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            delta_usd=round(delta, 4),
            spend_usd=round(self.spend.usd, 4),
        )
        return parsed
