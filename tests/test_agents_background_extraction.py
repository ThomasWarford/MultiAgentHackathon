"""Background + extraction agent unit tests.

Mock the AnthropicClient so we exercise the prompt-rendering and
output-binding paths without network. The LLM client itself is covered in
test_llm_client.py.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from matchmaker.agents.background import ResearcherBackgroundAgent
from matchmaker.agents.extraction import DimensionalExtractor
from matchmaker.schemas import (
    Publication,
    ResearcherBackground,
    ResearcherProfile,
    SummaryItem,
)


def _profile() -> ResearcherProfile:
    return ResearcherProfile(
        researcher_id="ada",
        display_name="Ada Lovelace",
        publications=[
            Publication(
                id="ada_1",
                title="On the Analytical Engine",
                source="local",
                source_id="ada_1.md",
                full_text_md="A note about symbolic computation and Bernoulli numbers.",
            ),
            Publication(
                id="ada_2",
                title="A Second Paper",
                source="local",
                source_id="ada_2.md",
                full_text_md="Discussion of mechanical recurrence.",
            ),
        ],
    )


class _FakeLLM:
    """Records prompts and returns a queued response."""

    def __init__(self, responses: list[BaseModel]) -> None:
        self._responses = list(responses)
        self.captured: list[dict[str, Any]] = []

    async def structured(self, **kwargs: Any) -> BaseModel:
        self.captured.append(kwargs)
        return self._responses.pop(0)


class TestResearcherBackgroundAgent:
    async def test_binds_researcher_id_and_renders_prompt(self) -> None:
        from matchmaker.agents.background import _BackgroundOutput

        llm = _FakeLLM(
            [
                _BackgroundOutput(
                    narrative="A narrative paragraph.",
                    keywords=["analytical-engine", "symbolic-computation"],
                )
            ]
        )
        agent = ResearcherBackgroundAgent(llm=llm, model="claude-haiku-4-5-20251001")  # type: ignore[arg-type]
        out = await agent.run(_profile())
        assert isinstance(out, ResearcherBackground)
        assert out.researcher_id == "ada"
        assert out.keywords == ["analytical-engine", "symbolic-computation"]
        # Prompt must include the researcher id and at least one publication id.
        rendered = llm.captured[0]["user"]
        assert "ada" in rendered
        assert "[ada_1]" in rendered


class TestDimensionalExtractor:
    @pytest.mark.parametrize("dim", ["methods", "open_questions", "stakes"])
    async def test_extractor_binds_dimension_and_id(self, dim) -> None:
        from matchmaker.agents.extraction import _ItemsOutput

        llm = _FakeLLM(
            [
                _ItemsOutput(
                    items=[
                        SummaryItem(
                            item_id="i1",
                            title=f"Title for {dim}",
                            description="A description.",
                            evidence=["ada_1"],
                        )
                    ]
                )
            ]
        )
        agent = DimensionalExtractor(
            llm=llm,  # type: ignore[arg-type]
            model="claude-haiku-4-5-20251001",
            dimension=dim,
        )
        profile = _profile()
        background = ResearcherBackground(
            researcher_id="ada",
            narrative="background prose",
            keywords=["x"],
        )
        result = await agent.run(profile, background)
        assert result.researcher_id == "ada"
        assert result.dimension == dim
        assert len(result.items) == 1
        assert result.items[0].item_id == "i1"
        # The dimension-specific prompt template must have been used.
        rendered = llm.captured[0]["user"]
        assert "background prose" in rendered
        assert "[ada_1]" in rendered
