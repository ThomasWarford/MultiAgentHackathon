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
    papers_text: str
    context: str        # optional external context from a previous step
    methods: str
    open_questions: str
    significance: str
    summary: str


# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

METHODS_PROMPT = (
    "You are an expert research analyst. "
    "Given the following research papers by a single researcher, "
    "write a structured markdown section titled '## Methods' that identifies "
    "the core methodological approaches, tools, datasets, and experimental or "
    "theoretical frameworks this researcher uses across their body of work."
)

OPEN_QUESTIONS_PROMPT = (
    "You are an expert research analyst. "
    "Given the following research papers, write a structured markdown section "
    "titled '## Open Questions' that enumerates the key unsolved problems, "
    "bottlenecks, stated limitations, and future directions the researcher "
    "explicitly or implicitly surfaces."
)

SIGNIFICANCE_PROMPT = (
    "You are an expert research analyst. "
    "Given the following research papers, write a structured markdown section "
    "titled '## Significance & Stakes' covering the real-world impact, "
    "scientific importance, and motivating challenges behind this researcher's work."
)

SUMMARY_PROMPT = (
    "You are an expert research analyst. "
    "Given three analytical sections about a researcher's body of work, "
    "write a concise markdown summary titled '## Summary' (3–5 paragraphs) "
    "that a collaborator from a different field can quickly read to understand "
    "who this person is and where collaboration might be fruitful."
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
            HumanMessage(content=state["papers_text"]),
        ]
        return {section_key: llm.invoke(messages).content}

    node.__name__ = f"{section_key}_node"
    return node


# ---------------------------------------------------------------------------
# Summary node (reads section outputs, not raw papers)
# ---------------------------------------------------------------------------

def summary_node(state: ResearcherState) -> dict:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    context_block = (
        f"\n\n## Additional context\n{state['context']}" if state["context"] else ""
    )
    synthesis = (
        f"{state['methods']}\n\n"
        f"{state['open_questions']}\n\n"
        f"{state['significance']}"
    )
    messages = [
        SystemMessage(content=SUMMARY_PROMPT + context_block),
        HumanMessage(content=synthesis),
    ]
    return {"summary": llm.invoke(messages).content}


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def build_graph(sequential: bool = False) -> object:
    methods_node = make_section_agent("methods", METHODS_PROMPT)
    open_questions_node = make_section_agent("open_questions", OPEN_QUESTIONS_PROMPT)
    significance_node = make_section_agent("significance", SIGNIFICANCE_PROMPT)

    graph = StateGraph(ResearcherState)
    graph.add_node("methods", methods_node)
    graph.add_node("open_questions", open_questions_node)
    graph.add_node("significance", significance_node)
    graph.add_node("summary", summary_node)

    if sequential:
        graph.add_edge(START, "methods")
        graph.add_edge("methods", "open_questions")
        graph.add_edge("open_questions", "significance")
        graph.add_edge("significance", "summary")
    else:
        graph.add_edge(START, "methods")
        graph.add_edge(START, "open_questions")
        graph.add_edge(START, "significance")
        graph.add_edge("methods", "summary")
        graph.add_edge("open_questions", "summary")
        graph.add_edge("significance", "summary")

    graph.add_edge("summary", END)
    return graph.compile()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_researcher_overview(
    name: str,
    context: str = "",
    sequential: bool = False,
) -> None:
    papers_dir = Path("papers") / name
    papers_text = "\n\n---\n\n".join(
        p.read_text(encoding="utf-8") for p in sorted(papers_dir.glob("*.md"))
    )

    initial_state: ResearcherState = {
        "name": name,
        "papers_text": papers_text,
        "context": context,
        "methods": "",
        "open_questions": "",
        "significance": "",
        "summary": "",
    }

    app = build_graph(sequential=sequential)
    final_state = app.invoke(initial_state)

    out_dir = Path("researcher_overview") / name
    out_dir.mkdir(parents=True, exist_ok=True)
    for key in ("methods", "open_questions", "significance", "summary"):
        (out_dir / f"{key}.md").write_text(final_state[key], encoding="utf-8")
        print(f"  wrote researcher_overview/{name}/{key}.md")


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
