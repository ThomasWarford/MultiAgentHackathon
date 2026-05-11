You are analyzing one cell of a cross-factorial matrix between two researchers, looking for a non-obvious **transfer opportunity** across their work.

# Researcher A — {display_a}
Dimension: **{dim_a}**

Items:
{items_a_block}

# Researcher B — {display_b}
Dimension: **{dim_b}**

Items:
{items_b_block}

# Your task
Produce a single **ConnectionCell** describing the relationship between A's `{dim_a}` and B's `{dim_b}`.

Fields:
- `items_a`: subset of A's item_ids above that are actually involved in the connection (may be empty).
- `items_b`: same for B (may be empty).
- `connection_type`: one of:
    - `method_transfer` — A's tool can address B's question (or vice versa).
    - `shared_stake` — both stake on the same outcome from different angles.
    - `complementary_gap` — A's open question is B's blind spot, or vice versa.
    - `analogous_pattern` — different domains, isomorphic structure.
    - `no_meaningful_link` — explicit null result; no substantive connection visible.
- `rationale`: 3-6 sentences. Be concrete. Name the items on each side and explain the bridge. If `no_meaningful_link`, briefly say why (and pick a non-zero confidence).
- `novelty_score`: 0..1. How surprising / non-obvious is this connection?
- `confidence`: 0..1. How well-supported is the connection by the items?

It is OK and important to return `no_meaningful_link` for cells where no real bridge exists — false-positive connections poison downstream synthesis. Prefer null over confabulation.
