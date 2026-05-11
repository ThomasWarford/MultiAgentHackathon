"""CLI entry point.

`matchmaker run --a csanyi --b pellegrini` is the demo command. It builds the
full pipeline, runs it end-to-end, writes per-stage JSON artifacts under
outputs/<stage>/, and emits a human-readable markdown report.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

import typer

from matchmaker import __version__
from matchmaker.config import load_settings
from matchmaker.logging import configure_logging, get_logger
from matchmaker.runner import run_match_async, write_all_artifacts

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
        openai_configured=bool(settings.openai_api_key),
        denario_configured=bool(settings.denario_base_url and settings.denario_api_key),
    )


@app.command()
def web(
    host: str = typer.Option("127.0.0.1", help="Host interface for the browser UI."),
    port: int = typer.Option(8000, help="Port for the browser UI."),
) -> None:
    """Launch a browser-based interface for running researcher matches."""
    from matchmaker.web import run_web_server

    run_web_server(host=host, port=port)


@app.command()
def run(
    researcher_a: str = typer.Option(..., "--a", help="First researcher's slug (matches papers/<slug>/)."),
    researcher_b: str = typer.Option(..., "--b", help="Second researcher's slug."),
    prompts_dir: Optional[Path] = typer.Option(None, help="Directory with <slug>.md ResearcherPrompts."),
    backend: Optional[str] = typer.Option(None, help="Refinement backend: mock | local | denario."),
    papers_dir: Optional[Path] = typer.Option(None, help="Papers corpus root."),
    outputs_dir: Optional[Path] = typer.Option(None, help="Where stage artifacts are written."),
    run_id: Optional[str] = typer.Option(None, help="Custom run id; auto-generated if omitted."),
) -> None:
    """Run the full pipeline end-to-end for two researchers."""
    asyncio.run(
        _run_async(
            researcher_a=researcher_a,
            researcher_b=researcher_b,
            prompts_dir=prompts_dir,
            backend=backend,
            papers_dir=papers_dir,
            outputs_dir=outputs_dir,
            run_id=run_id,
        )
    )


async def _run_async(
    *,
    researcher_a: str,
    researcher_b: str,
    prompts_dir: Optional[Path],
    backend: Optional[str],
    papers_dir: Optional[Path],
    outputs_dir: Optional[Path],
    run_id: Optional[str],
) -> None:
    report_path = await run_match_async(
        researcher_a=researcher_a,
        researcher_b=researcher_b,
        prompts_dir=prompts_dir,
        backend=backend,
        papers_dir=papers_dir,
        outputs_dir=outputs_dir,
        run_id=run_id,
    )
    typer.echo(f"\nReport written to: {report_path}")


def _write_all_artifacts(*args, **kwargs) -> None:
    write_all_artifacts(*args, **kwargs)


if __name__ == "__main__":
    app()
