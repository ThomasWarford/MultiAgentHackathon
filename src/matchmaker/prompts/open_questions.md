You are extracting the **Open Questions** dimension of a researcher's profile — the unresolved scientific puzzles they are working on or have explicitly flagged.

# Researcher
- ID: {researcher_id}
- Display name: {display_name}

# Researcher background (already distilled)
{background_narrative}

# Publications (truncated)
{publications_block}

# Your task
Identify 5-10 distinct **open questions** items. For each item:
- `item_id`: a short stable slug, e.g. "long-range-electrostatics", "soc-decomposition-rates". Lowercase, hyphenated.
- `title`: 5-12 word descriptor phrased as a question or unsettled topic.
- `description`: 2-4 sentences. Make explicit what's not yet known, what would constitute progress, and why the question is hard.
- `evidence`: list of Publication.id values where the question surfaces. Use only IDs from the publications block.

Prefer questions that the researcher themselves has flagged (limitations sections, future-work statements) over questions you infer from outside. Avoid generic "more work is needed" framings — be specific.
