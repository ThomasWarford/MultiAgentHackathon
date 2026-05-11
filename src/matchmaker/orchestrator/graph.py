"""LangGraph wiring.

Linear DAG; the only adaptive behavior (the bounded review→refine loop) lives
inside the refine_loop node itself, not as a graph-level conditional edge.
That keeps the graph shape stable and predictable; recursion_limit is set
generously as a safety net only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from langgraph.graph import END, START, StateGraph

from matchmaker.agents.llm import OpenAIClient
from matchmaker.config import Settings
from matchmaker.ingestion import Source
from matchmaker.orchestrator.nodes import (
    make_background_node,
    make_cross_factorial_node,
    make_extraction_node,
    make_hypotheses_node,
    make_ingest_node,
    make_load_prompts_node,
    make_rank_node,
    make_refine_loop_node,
)
from matchmaker.refinement import RefinementStack
from matchmaker.schemas import PipelineState

_RECURSION_LIMIT = 50


@dataclass
class GraphContext:
    """Resources every node closes over. Built once per run."""

    settings: Settings
    llm: OpenAIClient
    source: Source
    stack: RefinementStack
    researcher_a_id: str
    researcher_b_id: str
    prompts_dir: Path


def build_graph(ctx: GraphContext):
    g: StateGraph = StateGraph(PipelineState)

    g.add_node("ingest", make_ingest_node(ctx))
    g.add_node("background", make_background_node(ctx))
    g.add_node("extract_dimensions", make_extraction_node(ctx))
    g.add_node("cross_factorial", make_cross_factorial_node(ctx))
    g.add_node("load_prompts", make_load_prompts_node(ctx))
    g.add_node("hypotheses", make_hypotheses_node(ctx))
    g.add_node("refine_loop", make_refine_loop_node(ctx))
    g.add_node("rank", make_rank_node(ctx))

    g.add_edge(START, "ingest")
    g.add_edge("ingest", "background")
    g.add_edge("background", "extract_dimensions")
    g.add_edge("extract_dimensions", "cross_factorial")
    g.add_edge("cross_factorial", "load_prompts")
    g.add_edge("load_prompts", "hypotheses")
    g.add_edge("hypotheses", "refine_loop")
    g.add_edge("refine_loop", "rank")
    g.add_edge("rank", END)

    return g.compile()


__all__ = ["GraphContext", "build_graph", "_RECURSION_LIMIT"]
