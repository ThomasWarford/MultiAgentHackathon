# Researcher Matchmaking / Collaboration Assistant

## Goal / Vision
An agentic workflow that connects two (or more) researchers and finds good topics for collaboration.

## Use Cases
- Early career researchers in new department: run for everyone in the department.
- Get around the jargon that makes finding common ground difficult.
- Extract open questions: answer with LLM and find other researchers who can help.

---

## Pipeline Overview

The project has two stages:

### Stage 1 — Per-researcher overviews (`agent_researcher_overview.py`)

Processes each researcher's papers individually (one paper at a time to stay within context limits) using four parallel LangGraph agents. Outputs four markdown files per researcher:

```
researcher_overview/<name>/
    methods.md          # methodological approaches, tools, datasets
    open_questions.md   # unsolved problems, bottlenecks, future directions
    significance.md     # real-world impact and motivating challenges
    summary.md          # concise per-paper summaries for non-specialists
```

Each file has a `### <paper-name>` section per paper.

Run with:
```bash
python agent_researcher_overview.py csanyi pellegrini
# or to process all researchers in papers/:
python agent_researcher_overview.py
```

### Stage 2 — Cross-researcher overlap (`matchmaker` CLI)

An 8-stage LangGraph pipeline that takes two researchers and finds collaboration opportunities:

| Stage | Node | What it does |
|-------|------|--------------|
| 1 | `ingest` | Reads papers from `papers/<name>/` |
| 2 | `background` | Synthesises a researcher background summary |
| 3 | `extract_dimensions` | Extracts methods / open questions / stakes per researcher |
| 4 | `cross_factorial` | Builds a 3×3 overlap matrix between the two researchers |
| 5 | `load_prompts` | Loads researcher context from `prompts_input/<name>.md` |
| 6 | `hypotheses` | Generates specific collaboration hypotheses from the matrix |
| 7 | `refine_loop` | Review → refine cycle for each hypothesis (mock by default) |
| 8 | `rank` | Ranks refined hypotheses by confidence |

Outputs are written to `outputs/` and a final markdown report to `outputs/report/<run-id>.md`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+ / conda env `hack`
- `OPENAI_API_KEY` in `.env`

### Installation

```bash
# Install the matchmaker package in development mode
pip install -e ".[dev]"
```

### Environment Variables

Add to `.env`:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Required for all LLM stages |
| `DENARIO_BASE_URL` / `DENARIO_API_KEY` | Only needed when `MATCHMAKER_REFINEMENT_BACKEND=denario` |

### Researcher prompt files (required for Stage 2)

Create `prompts_input/<name>.md` for each researcher with at least a `## Current focus` section:

```markdown
## Current focus
One paragraph describing what this researcher is currently working on.

## Recent milestones
- Key result 1
- Key result 2

## Blockers
- Open challenge 1
```

### Running Stage 1 (per-researcher overviews)

```bash
python agent_researcher_overview.py csanyi pellegrini
```

### Running Stage 2 (cross-researcher matchmaking)

```bash
matchmaker run --a csanyi --b pellegrini
```

Output report: `outputs/report/<run-id>.md`

### Model selection

Defaults in `src/matchmaker/config.py` use the cheap tier to keep test runs inexpensive. Override per-stage via env vars (`MATCHMAKER_MODEL_BACKGROUND`, etc.) or by editing `config.py`:

| Setting | Stage | Default |
|---------|-------|---------|
| `model_background` | 2 — researcher synthesis | `gpt-4o-mini` |
| `model_extraction` | 3 — dimensions fan-out | `gpt-4o-mini` |
| `model_cross_factorial` | 4 — 9-cell matrix | `gpt-4o-mini` |
| `model_hypotheses` | 6 — hypothesis synthesis | `gpt-4o-mini` |
| `model_refinement` | 7 — review + refine | `gpt-4o-mini` |
| `model_ranking` | 8 — final ranking | `gpt-4o-mini` |

The cost ceiling (`MATCHMAKER_COST_CEILING_USD`, default `$5.00`) is enforced before every LLM call.

---

## 📁 Project Structure

```
MultiAgentHackathon/
├── agent_researcher_overview.py   # Stage 1: per-researcher 4-file overviews
├── papers/                        # Pre-converted markdown papers
│   ├── csanyi/
│   └── pellegrini/
├── researcher_overview/           # Stage 1 outputs (generated)
├── prompts_input/                 # Researcher context files for Stage 2
├── outputs/                       # Stage 2 artifacts + final report (generated)
├── src/matchmaker/                # Stage 2 matchmaking package
│   ├── agents/                    # LLM agent implementations
│   ├── orchestrator/              # LangGraph graph + nodes
│   ├── refinement/                # Review/refine/rank backends
│   ├── schemas/                   # Pydantic models
│   └── prompts/                   # Prompt templates
├── tests/
├── utils/pdf_to_markdown.py       # PDF → markdown conversion
└── pyproject.toml
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🛣️ Roadmap

- [ ] Milestone 1 – MVP demo
- [ ] Milestone 2 – Add memory / persistence
- [ ] Milestone 3 – Deploy to cloud

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👥 Team

| Name | Role | GitHub |
|------|------|--------|
| Your Name | Lead Developer | [@handle](https://github.com/handle) |

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- Any other libraries, datasets, or inspirations
