"""Unit tests for the LLM client wrapper.

These exercise the cost accounting and structured-output decoding without
calling the network — the OpenAI client is monkey-patched.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from matchmaker.agents.llm import (
    MODEL_PRICING,
    CostCeilingExceeded,
    OpenAIClient,
    TokenSpend,
)


class Echo(BaseModel):
    """Trivial response model for tests."""

    word: str


class FakeChatCompletions:
    def __init__(
        self,
        parsed: BaseModel,
        in_tok: int = 100,
        out_tok: int = 50,
    ) -> None:
        self._parsed = parsed
        self._in = in_tok
        self._out = out_tok

    async def parse(self, **kwargs):  # noqa: ANN003 — mirror SDK signature
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(parsed=self._parsed, refusal=None),
                    finish_reason="stop",
                )
            ],
            usage=SimpleNamespace(
                prompt_tokens=self._in, completion_tokens=self._out
            ),
        )


class FakeOpenAI:
    """Mirrors the bits of AsyncOpenAI that OpenAIClient.structured touches."""

    def __init__(
        self,
        parsed: BaseModel,
        in_tok: int = 100,
        out_tok: int = 50,
    ) -> None:
        completions = FakeChatCompletions(parsed, in_tok, out_tok)
        self.beta = SimpleNamespace(
            chat=SimpleNamespace(completions=completions)
        )


class TestTokenSpend:
    def test_mini_pricing_math(self) -> None:
        spend = TokenSpend()
        delta = spend.add("gpt-4o-mini", 1_000_000, 1_000_000)
        # (1M * $0.15 + 1M * $0.60) / 1M = $0.75
        assert pytest.approx(delta, rel=1e-6) == 0.75
        assert spend.usd == pytest.approx(0.75)
        assert spend.calls == 1
        assert spend.by_model["gpt-4o-mini"] == pytest.approx(0.75)

    def test_unknown_model_uses_fallback(self) -> None:
        spend = TokenSpend()
        delta = spend.add("gpt-unknown", 1_000_000, 0)
        assert delta == pytest.approx(5.0)  # fallback input rate


class TestOpenAIClient:
    def test_constructor_requires_api_key(self) -> None:
        with pytest.raises(ValueError):
            OpenAIClient(api_key="", cost_ceiling_usd=1.0)

    async def test_structured_parses_response_and_tracks_spend(self) -> None:
        client = OpenAIClient(api_key="dummy", cost_ceiling_usd=1.0)
        client._client = FakeOpenAI(Echo(word="hello"))  # type: ignore[assignment]

        out = await client.structured(
            model="gpt-4o-mini",
            system="sys",
            user="usr",
            response_model=Echo,
        )
        assert out == Echo(word="hello")
        assert client.spend.calls == 1
        assert client.spend.usd > 0

    async def test_cost_ceiling_blocks_further_calls(self) -> None:
        client = OpenAIClient(api_key="dummy", cost_ceiling_usd=0.0001)
        client._client = FakeOpenAI(  # type: ignore[assignment]
            Echo(word="x"), in_tok=1_000_000, out_tok=1_000_000
        )

        # First call goes through (spend starts at 0).
        await client.structured(
            model="gpt-4o-mini",
            system="s",
            user="u",
            response_model=Echo,
        )
        # Second call must trip the breaker since spend is now well over ceiling.
        with pytest.raises(CostCeilingExceeded):
            await client.structured(
                model="gpt-4o-mini",
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
