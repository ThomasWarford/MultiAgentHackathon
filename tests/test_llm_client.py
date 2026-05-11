"""Unit tests for the LLM client wrapper.

These exercise the cost accounting and structured-output decoding without
calling the network — the Anthropic client is monkey-patched.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from matchmaker.agents.llm import (
    MODEL_PRICING,
    AnthropicClient,
    CostCeilingExceeded,
    TokenSpend,
)


class Echo(BaseModel):
    """Trivial response model for tests."""

    word: str


class FakeMessages:
    def __init__(self, tool_input: dict, in_tok: int = 100, out_tok: int = 50) -> None:
        self._input = tool_input
        self._in = in_tok
        self._out = out_tok

    async def create(self, **kwargs):  # noqa: ANN003 — mirror SDK signature
        tool_name = kwargs["tools"][0]["name"]
        return SimpleNamespace(
            content=[
                SimpleNamespace(type="tool_use", name=tool_name, input=self._input),
            ],
            usage=SimpleNamespace(input_tokens=self._in, output_tokens=self._out),
        )


class FakeAnthropic:
    def __init__(self, tool_input: dict, in_tok: int = 100, out_tok: int = 50) -> None:
        self.messages = FakeMessages(tool_input, in_tok, out_tok)


class TestTokenSpend:
    def test_haiku_pricing_math(self) -> None:
        spend = TokenSpend()
        delta = spend.add("claude-haiku-4-5-20251001", 1_000_000, 1_000_000)
        # (1M * $1 + 1M * $5) / 1M = $6
        assert pytest.approx(delta, rel=1e-6) == 6.0
        assert spend.usd == pytest.approx(6.0)
        assert spend.calls == 1
        assert spend.by_model["claude-haiku-4-5-20251001"] == pytest.approx(6.0)

    def test_unknown_model_uses_fallback(self) -> None:
        spend = TokenSpend()
        delta = spend.add("claude-unknown", 1_000_000, 0)
        assert delta == pytest.approx(5.0)  # fallback input rate


class TestAnthropicClient:
    def test_constructor_requires_api_key(self) -> None:
        with pytest.raises(ValueError):
            AnthropicClient(api_key="", cost_ceiling_usd=1.0)

    async def test_structured_parses_tool_use_and_tracks_spend(self, monkeypatch) -> None:
        client = AnthropicClient(api_key="dummy", cost_ceiling_usd=1.0)
        client._client = FakeAnthropic({"word": "hello"})  # type: ignore[assignment]

        out = await client.structured(
            model="claude-haiku-4-5-20251001",
            system="sys",
            user="usr",
            response_model=Echo,
        )
        assert out == Echo(word="hello")
        assert client.spend.calls == 1
        assert client.spend.usd > 0

    async def test_cost_ceiling_blocks_further_calls(self, monkeypatch) -> None:
        client = AnthropicClient(api_key="dummy", cost_ceiling_usd=0.0001)
        client._client = FakeAnthropic({"word": "x"}, in_tok=1_000_000, out_tok=1_000_000)

        # First call goes through (spend starts at 0).
        await client.structured(
            model="claude-haiku-4-5-20251001",
            system="s",
            user="u",
            response_model=Echo,
        )
        # Second call must trip the breaker since spend is now well over ceiling.
        with pytest.raises(CostCeilingExceeded):
            await client.structured(
                model="claude-haiku-4-5-20251001",
                system="s",
                user="u",
                response_model=Echo,
            )


def test_all_default_models_have_pricing() -> None:
    """Settings defaults must be priced — otherwise the budget is silently wrong."""
    from matchmaker.config import Settings

    s = Settings()
    for model in {
        s.model_background,
        s.model_extraction,
        s.model_cross_factorial,
        s.model_hypotheses,
        s.model_refinement,
        s.model_ranking,
    }:
        assert model in MODEL_PRICING, f"missing pricing for {model}"
