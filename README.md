# Researcher Matchmaking / Collaboration Assistant

## Goal / Vision
An agentic workflow that connects two (or more) researchers and finds good topics for collaboration.


## Use Cases
- Early career researchers in new department: run for everyone in the department.
- Get around the jargon that makes finding common ground difficult.
- Extract open questions: answer with LLM and find other researchers who can help.
---
## Design
- Publication scraper
- Papers -> summary
  - Methods
  - Look for open questions
- Should get across things you wouldn't be able get accross in a conversation / CV.

### Wishlist
- Go through references
- Multiple researchers (by department, ect.)
- Conversation recordings
- Researcher prompts


## 🏗️ Architecture

Describe the high-level multi-agent architecture here. Include a diagram if possible.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Agent A    │────▶│ Orchestrator│────▶│  Agent B    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Agents

| Agent | Role | Model / Framework |
|-------|------|-------------------|
| Agent A | Description | e.g. GPT-4o |
| Agent B | Description | e.g. Claude 3.5 |
| Orchestrator | Coordinates agents | e.g. LangGraph |

---

## ✨ Features

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- (List other dependencies, e.g. Docker, Node.js, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/MultiAgentHackathon.git
cd MultiAgentHackathon

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Copy the example env file and fill in your API keys:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key (required for stages 1-6 and the `local` refinement backend) |
| `DENARIO_BASE_URL` / `DENARIO_API_KEY` | Only required when `MATCHMAKER_REFINEMENT_BACKEND=denario` (stages 7-8) |

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
python main.py
```

---

## 📁 Project Structure

```
MultiAgentHackathon/
├── agents/             # Individual agent definitions
├── tools/              # Shared tools / utilities used by agents
├── orchestrator/       # Orchestration logic
├── tests/              # Unit & integration tests
├── .env.example        # Example environment variable file
├── requirements.txt    # Python dependencies
└── main.py             # Entry point
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
