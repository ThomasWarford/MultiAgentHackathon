"""Shared Anthropic client.

Every Stage 1-6 agent calls `AnthropicClient.structured(...)` with a Pydantic
response_model. The client:
- forces structured output via tool-use bound to the model's JSON schema,
- updates a shared TokenSpend tracker after each call,
- raises CostCeilingExceeded before issuing a call that would push spend over
  the configured ceiling, so a runaway refinement loop terminates predictably,
- logs a structured event at every call boundary (CLAUDE.md handoff rule).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

from anthropic import AsyncAnthropic
from pydantic import BaseModel

from matchmaker.logging import get_logger

T = TypeVar("T", bound=BaseModel)

log = get_logger(__name__)


# USD per 1M tokens (ballpark; tune per current Anthropic pricing).
MODEL_PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-4-7": (15.0, 75.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
}


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


class AnthropicClient:
    def __init__(
        self,
        *,
        api_key: str,
        cost_ceiling_usd: float,
        spend: TokenSpend | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is empty; set it in .env.")
        self._client = AsyncAnthropic(api_key=api_key)
        self._ceiling = cost_ceiling_usd
        self.spend = spend or TokenSpend()

    async def structured(
        self,
        *,
        model: str,
        system: str,
        user: str,
        response_model: type[T],
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ) -> T:
        if self.spend.usd >= self._ceiling:
            raise CostCeilingExceeded(
                f"Spend ${self.spend.usd:.4f} >= ceiling ${self._ceiling:.4f}; "
                f"refusing further LLM calls."
            )

        tool_name = response_model.__name__
        tool = {
            "name": tool_name,
            "description": (response_model.__doc__ or f"Return a {tool_name}.").strip(),
            "input_schema": response_model.model_json_schema(),
        }

        log.info(
            "llm.call.start",
            model=model,
            response_model=tool_name,
            spend_usd=round(self.spend.usd, 4),
            temperature=temperature,
        )

        response = await self._client.messages.create(
            model=model,
            system=system,
            messages=[{"role": "user", "content": user}],
            tools=[tool],
            tool_choice={"type": "tool", "name": tool_name},
            temperature=temperature,
            max_tokens=max_tokens,
        )

        usage = response.usage
        delta = self.spend.add(model, usage.input_tokens, usage.output_tokens)

        for block in response.content:
            if getattr(block, "type", None) == "tool_use" and block.name == tool_name:
                parsed = response_model.model_validate(block.input)
                log.info(
                    "llm.call.done",
                    model=model,
                    response_model=tool_name,
                    input_tokens=usage.input_tokens,
                    output_tokens=usage.output_tokens,
                    delta_usd=round(delta, 4),
                    spend_usd=round(self.spend.usd, 4),
                )
                return parsed

        raise RuntimeError(
            f"Expected tool_use block named {tool_name!r} in Anthropic response."
        )
