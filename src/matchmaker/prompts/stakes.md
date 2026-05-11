You are extracting the **Stakes** dimension of a researcher's profile — the real-world or scientific outcomes whose success this researcher is invested in.

# Researcher
- ID: {researcher_id}
- Display name: {display_name}

# Researcher background (already distilled)
{background_narrative}

# Publications (truncated)
{publications_block}

# Your task
Identify 5-10 distinct **stakes** items. For each item:
- `item_id`: a short stable slug, e.g. "climate-policy-relevance", "drug-discovery-throughput". Lowercase, hyphenated.
- `title`: 5-12 word descriptor of what's at stake.
- `description`: 2-4 sentences. Spell out why this matters — who benefits, what decision changes, what enables progress elsewhere if it works.
- `evidence`: list of Publication.id values that demonstrate the stake. Use only IDs from the publications block.

Stakes are about *consequence*: the field that gets unlocked, the policy lever that gets pulled, the limit that gets pushed. They are NOT the same as methods (how) or questions (what's unknown).

If a stake is implicit rather than stated, infer it but flag tentatively in the description.
