# Matchmaker

Multi-agent research matchmaking workflow for finding concrete collaboration ideas between two researchers.

Matchmaker ingests local publication corpora, extracts each researcher's methods, open questions, and stakes, builds a 3x3 cross-factorial connection matrix, synthesizes candidate collaboration hypotheses, reviews/refines them, and writes a ranked Markdown report plus per-stage JSON artifacts.

## What It Does

- Reads pre-converted Markdown papers from `papers/<researcher_id>/*.md`.
- Reads explicit researcher priorities from `prompts_input/<researcher_id>.md`.
- Uses OpenAI structured outputs for the background, extraction, matrix, and hypothesis stages.
- Runs a bounded review/refine loop with one of three refinement backends: `mock`, `local`, or `denario`.
- Tracks estimated model spend and stops before exceeding `MATCHMAKER_COST_CEILING_USD`.
- Writes reproducible artifacts under `outputs/` and a final report under `outputs/report/`.

## Pipeline

```text
papers/<id>/*.md + prompts_input/<id>.md
        |
        v
LocalCorpusSource + prompt loader
        |
        v
Researcher backgrounds
        |
        v
Methods / open questions / stakes extraction
        |
        v
3x3 cross-factorial connection matrix
        |
        v
Collaboration hypothesis generation
        |
        v
Review -> refine loop
        |
        v
Ranking + final Markdown report
```

The LangGraph DAG is linear from ingestion through ranking. The adaptive behavior is inside the refinement node, where each hypothesis gets its own bounded asynchronous review/refine loop.

## Requirements

- Python 3.11+
- `uv` recommended, because the repository includes `uv.lock`
- An `OPENAI_API_KEY` for real pipeline runs

## Setup

```bash
uv sync --dev
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Required for all LLM stages |
| `DENARIO_BASE_URL` / `DENARIO_API_KEY` | Only needed when `MATCHMAKER_REFINEMENT_BACKEND=denario` |

### Model selection

All stages share a priced model catalogue defined in `src/matchmaker/agents/llm.py`
(`MODEL_PRICING`). Defaults in `src/matchmaker/config.py` are set to
`gpt-5.5` across every stage:

| Setting | Stage | Default | Suggested upgrade (quality) |
|---------|-------|---------|------------------------------|
| `model_background` | 2 — researcher synthesis | `gpt-5.5` | `gpt-4o` |
| `model_extraction` | 3 — methods/questions/stakes | `gpt-5.5` | `gpt-5.5` (high volume; keep cheap) |
| `model_cross_factorial` | 4 — 9-cell matrix | `gpt-5.5` | `gpt-5.5` (9 calls; keep cheap) |
| `model_hypotheses` | 6 — hypothesis synthesis | `gpt-5.5` | `gpt-4o` |
| `model_refinement` | 7 — review + refine loop | `gpt-5.5` | `gpt-4o` |
| `model_ranking` | 8 — final ranking | `gpt-5.5` | `gpt-4o` or `o1` |

Override per-stage by editing `Settings` in `config.py`. The cost ceiling
(`MATCHMAKER_COST_CEILING_USD`, default `$5.00`) is enforced before every
LLM call by `OpenAIClient`, so a runaway loop terminates predictably.

### Running the Project

```bash
OPENAI_API_KEY=...
MATCHMAKER_REFINEMENT_BACKEND=local
MATCHMAKER_COST_CEILING_USD=5.0
MATCHMAKER_MAX_ITERATIONS=3
```

`DENARIO_BASE_URL` and `DENARIO_API_KEY` are only needed when `MATCHMAKER_REFINEMENT_BACKEND=denario`.

## Inputs

### Papers

Each researcher needs a directory under `papers/`:

```text
papers/
  csanyi/
    paper-one.md
    paper-two.md
  pellegrini/
    paper-one.md
    paper-two.md
```

Each `.md` file becomes one publication. PDFs can be converted with:

```bash
uv run python utils/pdf_to_markdown.py
```

### Researcher Prompts

Create one prompt file per researcher:

```text
prompts_input/
  csanyi.md
  pellegrini.md
```

Minimum format:

```markdown
## Current focus
What this researcher is actively trying to do now.

## Recent milestones
- Optional bullet
- Optional bullet

## Blockers
- Optional blocker

## Notes
Optional free text.
```

`## Current focus` is required. Unknown `##` sections are preserved as extra free text.

## Run

Check configuration:

```bash
uv run matchmaker doctor
```

Run the demo pair already present in `papers/`:

```bash
uv run matchmaker run --a csanyi --b pellegrini
```

Or launch the browser interface:

```bash
uv run matchmaker web
```

Then open `http://127.0.0.1:8000`, enter two researcher slugs, and submit the
match. The final report is shown in the page and still written to
`outputs/report/`.

Useful options:

```bash
uv run matchmaker run \
  --a csanyi \
  --b pellegrini \
  --prompts-dir prompts_input \
  --papers-dir papers \
  --outputs-dir outputs \
  --backend local \
  --run-id demo
```

Available refinement backends:

- `mock`: deterministic reviewer/refiner/ranker implementations for smoke testing refinement plumbing.
- `local`: OpenAI-backed reviewer, refiner, and ranker.
- `denario`: external Denario reviewer, refiner, and ranker using `DENARIO_BASE_URL` and `DENARIO_API_KEY`.

## Outputs

A run writes JSON artifacts to:

```text
outputs/
  01_publications/
  02_backgrounds/
  03_dimensional/
  04_matrix/
  05_hypotheses/
  06_critiques/
  07_refined/
  08_ranking/
  report/<run_id>.md
```

The final report contains the cross-factorial matrix, ranked collaboration hypotheses, revision notes, and ranking methodology.

## Configuration

Settings are loaded from environment variables and `.env` via `src/matchmaker/config.py`.

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | empty | Required for OpenAI-backed stages. |
| `DENARIO_BASE_URL` | empty | Required for `denario` backend. |
| `DENARIO_API_KEY` | empty | Required for `denario` backend. |
| `MATCHMAKER_REFINEMENT_BACKEND` | `local` | `mock`, `local`, or `denario`. |
| `MATCHMAKER_COST_CEILING_USD` | `5.0` | Stops further LLM calls once projected spend exceeds the ceiling. |
| `MATCHMAKER_MAX_ITERATIONS` | `3` | Max review/refine iterations per hypothesis. |
| `MATCHMAKER_LOG_LEVEL` | `INFO` | Structured logging level. |

Model defaults live in `Settings`:

| Setting | Stage | Default |
| --- | --- | --- |
| `model_background` | Researcher background synthesis | `gpt-4o-mini` |
| `model_extraction` | Methods/questions/stakes extraction | `gpt-4o-mini` |
| `model_cross_factorial` | 3x3 connection matrix | `gpt-4o-mini` |
| `model_hypotheses` | Hypothesis synthesis | `gpt-4o-mini` |
| `model_refinement` | Review/refine loop | `gpt-4o-mini` |
| `model_ranking` | Final ranking | `gpt-4o-mini` |

Pricing assumptions are defined in `src/matchmaker/agents/llm.py`.

## Project Structure

```text
src/matchmaker/
  agents/          OpenAI-backed extraction and synthesis agents
  ingestion/       Local paper corpus and prompt loading
  io/              Artifact and report writers
  orchestrator/    LangGraph wiring and node functions
  prompts/         Prompt templates for each stage
  refinement/      Mock, local OpenAI, and Denario refinement stacks
  schemas/         Pydantic state and artifact schemas
  cli.py           Typer CLI entry point
tests/             Unit and smoke tests
utils/             PDF conversion utilities
```

## Testing

```bash
uv run pytest
```

The graph smoke test uses a mocked OpenAI client, so it exercises orchestration and artifact writing without network calls.

## Development Notes

- The installed console script is `matchmaker`.
- The default `papers_dir` is `papers`.
- The default `prompts_input_dir` is `prompts_input`.
- The default `outputs_dir` is `outputs`.
- `ARCHITECURE.md` contains a more detailed architecture handoff note.
