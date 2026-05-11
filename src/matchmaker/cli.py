"""CLI entry point.

`matchmaker run --a csanyi --b pellegrini` is the demo command. It builds the
full pipeline, runs it end-to-end, writes per-stage JSON artifacts under
outputs/<stage>/, and emits a human-readable markdown report.
"""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
from typing import Optional

import typer

from matchmaker import __version__
from matchmaker.agents.llm import AnthropicClient
from matchmaker.config import load_settings
from matchmaker.ingestion import LocalCorpusSource
from matchmaker.io import render_final_report, write_artifact
from matchmaker.logging import configure_logging, get_logger
from matchmaker.orchestrator import GraphContext, build_graph
from matchmaker.refinement import build_refinement_stack
from matchmaker.schemas import PipelineState

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
    log = get_logger(__name__)
    settings = load_settings()
    if backend:
        settings = settings.model_copy(update={"refinement_backend": backend})  # type: ignore[arg-type]

    effective_papers_dir = papers_dir or settings.papers_dir
    effective_prompts_dir = prompts_dir or settings.prompts_input_dir
    effective_outputs_dir = outputs_dir or settings.outputs_dir
    rid = run_id or f"run_{uuid.uuid4().hex[:8]}"

    source = LocalCorpusSource(effective_papers_dir)

    if settings.refinement_backend in {"mock"}:
        llm: AnthropicClient | None = None
    else:
        llm = AnthropicClient(
            api_key=settings.anthropic_api_key,
            cost_ceiling_usd=settings.cost_ceiling_usd,
        )

    # Stages 1-6 always need an LLM (unless backend is "mock" AND we also mock those).
    # In MVP the routing portion is real Claude; only refinement is swappable.
    if llm is None and settings.refinement_backend == "mock":
        # For mock-only end-to-end runs you must still supply an Anthropic key
        # for the upstream agents. Raise loudly so this isn't a silent surprise.
        llm = AnthropicClient(
            api_key=settings.anthropic_api_key,
            cost_ceiling_usd=settings.cost_ceiling_usd,
        )

    stack = build_refinement_stack(settings, llm=llm)

    ctx = GraphContext(
        settings=settings,
        llm=llm,
        source=source,
        stack=stack,
        researcher_a_id=researcher_a,
        researcher_b_id=researcher_b,
        prompts_dir=effective_prompts_dir,
    )
    graph = build_graph(ctx)

    initial = PipelineState(run_id=rid)
    log.info("run.start", run_id=rid, a=researcher_a, b=researcher_b, backend=settings.refinement_backend)

    final_dict = await graph.ainvoke(
        initial.model_dump(),
        config={"recursion_limit": 50},
    )
    final = PipelineState.model_validate(final_dict)
    final.token_spend_usd = llm.spend.usd

    _write_all_artifacts(effective_outputs_dir, rid, final)

    report = render_final_report(final)
    report_path = effective_outputs_dir / "report" / f"{rid}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    log.info(
        "run.done",
        run_id=rid,
        report=str(report_path),
        token_spend_usd=round(final.token_spend_usd, 4),
    )
    typer.echo(f"\nReport written to: {report_path}")


def _write_all_artifacts(outputs_dir: Path, run_id: str, state: PipelineState) -> None:
    write_artifact(
        outputs_dir, "01_publications", run_id,
        {"profile_a": state.profile_a, "profile_b": state.profile_b},
    )
    write_artifact(
        outputs_dir, "02_backgrounds", run_id,
        {"background_a": state.background_a, "background_b": state.background_b},
    )
    write_artifact(
        outputs_dir, "03_dimensional", run_id,
        {"dimensions_a": state.dimensions_a, "dimensions_b": state.dimensions_b},
    )
    if state.matrix:
        write_artifact(outputs_dir, "04_matrix", run_id, state.matrix)
    write_artifact(
        outputs_dir, "05_hypotheses", run_id,
        {"hypotheses": state.hypotheses, "prompt_a": state.prompt_a, "prompt_b": state.prompt_b},
    )
    write_artifact(
        outputs_dir, "06_critiques", run_id,
        state.critique_histories,
    )
    write_artifact(
        outputs_dir, "07_refined", run_id,
        {"refined_hypotheses": state.refined_hypotheses},
    )
    if state.ranking:
        write_artifact(outputs_dir, "08_ranking", run_id, state.ranking)


if __name__ == "__main__":
    app()
