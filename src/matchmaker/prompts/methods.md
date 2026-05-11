You are extracting the **Methods** dimension of a researcher's profile — the techniques, tools, datasets, and methodological patterns they actually use.

# Researcher
- ID: {researcher_id}
- Display name: {display_name}

# Researcher background (already distilled)
{background_narrative}

# Publications (truncated)
{publications_block}

# Your task
Identify 5-10 distinct **methods** items. For each item:
- `item_id`: a short stable slug, e.g. "mlip-training", "meta-regression". Lowercase, hyphenated.
- `title`: 5-12 word descriptor.
- `description`: 2-4 sentences. Be concrete — name the technique, the scale/scope, and what it's used for.
- `evidence`: list of Publication.id values that demonstrate this method. Use only IDs from the publications block.

Focus on what they DO, not what they study. "Density Functional Theory calculations on liquid water" is a method; "interest in water" is not.

Do not invent methods that aren't visible in the corpus.
