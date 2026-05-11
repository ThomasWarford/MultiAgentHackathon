from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

load_dotenv()

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class ResearcherState(TypedDict):
    name: str
    paper_text: str   # single paper content
    paper_name: str   # filename stem, used as section header
    context: str      # optional external context from a previous step
    methods: str
    open_questions: str
    significance: str
    summary: str


SECTION_KEYS = ("methods", "open_questions", "significance", "summary")


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

METHODS_PROMPT = (
    "You are an expert research analyst. "
    "Given the following single research paper, identify the core methodological "
    "approaches, tools, datasets, and experimental or theoretical frameworks used. "
    "Write a structured markdown section titled '## Methods'."
)

OPEN_QUESTIONS_PROMPT = (
    "You are an expert research analyst. "
    "Given the following single research paper, enumerate the key unsolved problems, "
    "bottlenecks, stated limitations, and future directions the authors explicitly "
    "or implicitly surface. "
    "Write a structured markdown section titled '## Open Questions'."
)

SIGNIFICANCE_PROMPT = (
    "You are an expert research analyst. "
    "Given the following single research paper, describe the real-world impact, "
    "scientific importance, and motivating challenges behind this work. "
    "Write a structured markdown section titled '## Significance & Stakes'."
)

SUMMARY_PROMPT = (
    "You are an expert research analyst. "
    "Given the following single research paper, write a concise markdown summary "
    "titled '## Summary' (2–3 paragraphs) that a collaborator from a different "
    "field can quickly read to understand the contribution and its relevance."
)


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------

def make_section_agent(
    section_key: str,
    system_prompt: str,
    model: str = "gpt-4o",
) -> Callable[[ResearcherState], dict]:
    llm = ChatOpenAI(model=model, temperature=0)

    def node(state: ResearcherState) -> dict:
        context_block = (
            f"\n\n## Additional context\n{state['context']}"
            if state["context"]
            else ""
        )
        messages = [
            SystemMessage(content=system_prompt + context_block),
            HumanMessage(content=state["paper_text"]),
        ]
        return {section_key: llm.invoke(messages).content}

    node.__name__ = f"{section_key}_node"
    return node


# ---------------------------------------------------------------------------
# Graph builder — runs once per paper
# ---------------------------------------------------------------------------

def build_paper_graph(sequential: bool = False) -> object:
    prompts = {
        "methods": METHODS_PROMPT,
        "open_questions": OPEN_QUESTIONS_PROMPT,
        "significance": SIGNIFICANCE_PROMPT,
        "summary": SUMMARY_PROMPT,
    }

    graph = StateGraph(ResearcherState)
    for key, prompt in prompts.items():
        graph.add_node(key, make_section_agent(key, prompt))

    if sequential:
        graph.add_edge(START, "methods")
        graph.add_edge("methods", "open_questions")
        graph.add_edge("open_questions", "significance")
        graph.add_edge("significance", "summary")
        graph.add_edge("summary", END)
    else:
        for key in SECTION_KEYS:
            graph.add_edge(START, key)
            graph.add_edge(key, END)

    return graph.compile()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_researcher_overview(
    name: str,
    context: str = "",
    sequential: bool = False,
) -> None:
    papers = sorted((Path("papers") / name).glob("*.md"))
    out_dir = Path("researcher_overview") / name
    out_dir.mkdir(parents=True, exist_ok=True)

    for key in SECTION_KEYS:
        (out_dir / f"{key}.md").write_text("", encoding="utf-8")

    app = build_paper_graph(sequential=sequential)

    for paper_path in papers:
        print(f"  processing {paper_path.name}...")
        state: ResearcherState = {
            "name": name,
            "paper_text": paper_path.read_text(encoding="utf-8"),
            "paper_name": paper_path.stem,
            "context": context,
            "methods": "",
            "open_questions": "",
            "significance": "",
            "summary": "",
        }
        result = app.invoke(state)

        for key in SECTION_KEYS:
            with (out_dir / f"{key}.md").open("a", encoding="utf-8") as f:
                f.write(f"\n\n### {paper_path.stem}\n\n{result[key]}")

        print(f"    updated all sections")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    args = sys.argv[1:]
    sequential = "--sequential" in args
    names = [a for a in args if not a.startswith("--")]
    if not names:
        names = [d.name for d in Path("papers").iterdir() if d.is_dir()]

    mode = "sequential" if sequential else "parallel"
    for researcher in names:
        print(f"Processing {researcher} ({mode})...")
        run_researcher_overview(researcher, sequential=sequential)
        print(f"Done: researcher_overview/{researcher}/")
