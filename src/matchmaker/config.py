"""Runtime configuration.

Everything here is overridable by environment variables prefixed with
MATCHMAKER_ (see .env). The Settings object is loaded once at startup
and threaded through the orchestrator state — no module-level singletons.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

RefinementBackend = Literal["mock", "local", "denario"]
ProtocolErrorPolicy = Literal["raise", "fallback_to_local"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MATCHMAKER_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    denario_base_url: str = Field(default="", validation_alias="DENARIO_BASE_URL")
    denario_api_key: str = Field(default="", validation_alias="DENARIO_API_KEY")

    # Cost-tiered defaults — cheap models for bulk fan-out, premium for
    # high-leverage synthesis.  See MODEL_PRICING in agents/llm.py.
    #
    # Cheap tier (gpt-4o-mini @ $0.15/$0.60 per 1M tokens):
    #   - background: 2 calls — straightforward narrative summarisation.
    #   - extraction: 6 calls (3 dims × 2 researchers) — structured extraction.
    #
    # Premium tier (gpt-5.5):
    #   - cross_factorial: 9 calls (3×3 matrix) — non-obvious connection spotting.
    #   - hypotheses: 1-2 calls — creative synthesis requiring nuance.
    #   - refinement: variable (review + refine loops) — adversarial critique.
    #   - ranking: 1 call — comparative scoring across candidates.
    model_background: str = "gpt-4o-mini"
    model_extraction: str = "gpt-4o-mini"
    model_cross_factorial: str = "gpt-5.5"
    model_hypotheses: str = "gpt-5.5"
    model_refinement: str = "gpt-5.5"
    model_ranking: str = "gpt-5.5"

    cost_ceiling_usd: float = 5.0
    max_iterations: int = 3
    refinement_backend: RefinementBackend = "local"
    on_protocol_error: ProtocolErrorPolicy = "fallback_to_local"

    log_level: str = "INFO"

    papers_dir: Path = Path("papers")
    prompts_input_dir: Path = Path("prompts_input")
    outputs_dir: Path = Path("outputs")
    prompt_templates_dir: Path = Path("src/matchmaker/prompts")


def load_settings() -> Settings:
    return Settings()
