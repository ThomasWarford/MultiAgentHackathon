"""Runtime configuration.

Everything here is overridable by environment variables prefixed with
MATCHMAKER_ (see .env.example). The Settings object is loaded once at startup
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

    # Default to the cheap tier across the board so test runs stay inexpensive.
    # When you want higher quality (typically for stages 6-8), swap individual
    # entries to "gpt-4o" — see MODEL_PRICING in agents/llm.py for the full
    # priced catalogue. Stage rationale:
    #   - background / extraction / cross_factorial: high-volume fan-out
    #     (the matrix alone is 9 calls), keep on the cheap tier.
    #   - hypotheses / refinement / ranking: lower volume, higher leverage —
    #     candidates for "gpt-4o" once the pipeline is stable.
    model_background: str = "gpt-4o-mini"
    model_extraction: str = "gpt-4o-mini"
    model_cross_factorial: str = "gpt-4o-mini"
    model_hypotheses: str = "gpt-4o-mini"
    model_refinement: str = "gpt-4o-mini"
    model_ranking: str = "gpt-4o-mini"

    cost_ceiling_usd: float = 5.0
    max_iterations: int = 3
    refinement_backend: RefinementBackend = "mock"
    on_protocol_error: ProtocolErrorPolicy = "fallback_to_local"

    log_level: str = "INFO"

    papers_dir: Path = Path("papers")
    prompts_input_dir: Path = Path("prompts_input")
    outputs_dir: Path = Path("outputs")
    prompt_templates_dir: Path = Path("src/matchmaker/prompts")


def load_settings() -> Settings:
    return Settings()
