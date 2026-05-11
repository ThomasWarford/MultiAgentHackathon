"""CLI entry point. Fleshed out incrementally as stages land."""

from __future__ import annotations

import typer

from matchmaker import __version__
from matchmaker.config import load_settings
from matchmaker.logging import configure_logging, get_logger

app = typer.Typer(help="Multi-agent research matchmaking workflow.")


@app.callback()
def _root() -> None:
    settings = load_settings()
    configure_logging(settings.log_level)


@app.command()
def version() -> None:
    """Print the installed matchmaker version."""
    typer.echo(__version__)


@app.command()
def doctor() -> None:
    """Print loaded config so you can verify env wiring."""
    settings = load_settings()
    log = get_logger(__name__)
    log.info(
        "settings.loaded",
        refinement_backend=settings.refinement_backend,
        cost_ceiling_usd=settings.cost_ceiling_usd,
        max_iterations=settings.max_iterations,
        anthropic_configured=bool(settings.anthropic_api_key),
        denario_configured=bool(settings.denario_base_url and settings.denario_api_key),
    )


if __name__ == "__main__":
    app()
