"""Human-readable markdown report rendered after a run completes.

Designed to be scannable by hackathon judges: the cross-factorial matrix
collapsed into a 3x3 grid with one-line cell summaries, then the ranked
hypotheses in order.
"""

from __future__ import annotations

from matchmaker.schemas import DIMS, CrossFactorialMatrix, PipelineState


def _matrix_grid(matrix: CrossFactorialMatrix) -> str:
    header = "| A \\ B | " + " | ".join(DIMS) + " |"
    sep = "|" + "---|" * (len(DIMS) + 1)
    rows = [header, sep]
    for a in DIMS:
        cells = []
        for b in DIMS:
            c = matrix.get(a, b)
            tag = c.connection_type.replace("_", " ")
            cells.append(f"{tag} ({c.novelty_score:.2f}/{c.confidence:.2f})")
        rows.append(f"| **{a}** | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def _matrix_details(matrix: CrossFactorialMatrix) -> str:
    parts: list[str] = []
    for c in matrix.cells:
        parts.append(
            f"### [{c.dim_a} × {c.dim_b}] — {c.connection_type}\n\n"
            f"- Novelty: {c.novelty_score:.2f}, Confidence: {c.confidence:.2f}\n"
            f"- A items: {', '.join(c.items_a) or '_none_'}\n"
            f"- B items: {', '.join(c.items_b) or '_none_'}\n\n"
            f"{c.rationale}"
        )
    return "\n\n".join(parts)


def render_final_report(state: PipelineState) -> str:
    assert state.matrix and state.ranking and state.profile_a and state.profile_b

    a_name = state.profile_a.display_name
    b_name = state.profile_b.display_name

    refined_by_id = {h.hypothesis_id: h for h in state.refined_hypotheses}
    parts: list[str] = []
    parts.append(f"# Matchmaking report: {a_name} × {b_name}\n")
    parts.append(f"_Run `{state.run_id}` · token spend ${state.token_spend_usd:.4f}_\n")

    parts.append("## Cross-factorial matrix (type · novelty / confidence)\n")
    parts.append(_matrix_grid(state.matrix) + "\n")

    parts.append("## Top hypotheses\n")
    for r in state.ranking.items:
        h = refined_by_id.get(r.hypothesis_id)
        if h is None:
            continue
        dim_scores = ", ".join(f"{k}={v:.2f}" for k, v in sorted(r.dimension_scores.items()))
        parts.append(
            f"### #{r.rank} — {h.title}  \n"
            f"_id: `{h.hypothesis_id}` · composite {r.composite_score:.2f} · {dim_scores}_\n\n"
            f"**Statement.** {h.statement}\n\n"
            f"**Mechanism.** {h.mechanism}\n\n"
            f"**Leverages cells.** "
            + (", ".join(f"({a},{b})" for a, b in h.leverages_cells) or "_none_")
            + "\n\n"
            f"**Addresses prompts.** {', '.join(h.addresses_prompts) or '_none_'}\n\n"
            f"**Revision notes.** {h.revision_notes}\n\n"
            f"**Ranker justification.** {r.justification}\n"
        )

    parts.append("## Connection matrix details\n")
    parts.append(_matrix_details(state.matrix))

    parts.append("\n## Ranker methodology\n")
    parts.append(state.ranking.methodology)

    return "\n".join(parts)
