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

    anthropic_api_key: str = Field(default="", validation_alias="ANTHROPIC_API_KEY")
    denario_base_url: str = Field(default="", validation_alias="DENARIO_BASE_URL")
    denario_api_key: str = Field(default="", validation_alias="DENARIO_API_KEY")

    model_background: str = "claude-sonnet-4-6"
    model_extraction: str = "claude-haiku-4-5-20251001"
    model_cross_factorial: str = "claude-haiku-4-5-20251001"
    model_hypotheses: str = "claude-opus-4-7"
    model_refinement: str = "claude-opus-4-7"
    model_ranking: str = "claude-opus-4-7"

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
