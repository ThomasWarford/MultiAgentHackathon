You are ranking refined collaborative research hypotheses.

# Refined hypotheses
{hypotheses_block}

# Your task
Rank ALL hypotheses from best to worst. For each, score on these dimensions (each ∈ [0,1]):
- `novelty` — how non-obvious is the connection?
- `feasibility` — could the named experiment / deliverable plausibly be executed by the two researchers in 6-18 months?
- `falsifiability` — is the statement actually refutable?
- `stake_alignment` — does it advance at least one researcher's stated stakes/blockers?
- `evidence_grounding` — is it tied to specific matrix cells and items, or hand-wavy?

For each ranked entry produce:
- `hypothesis_id`
- `rank` (1 = best; integers, strictly increasing)
- `composite_score` ∈ [0,1] — your overall weight (your weighting choice goes in `methodology`).
- `dimension_scores` — dict including the 5 dimensions above.
- `justification` — 2-4 sentences citing concrete reasons drawn from the hypothesis.

In `methodology`, in 1-3 sentences, state how you weighted the dimensions (e.g., "weighted falsifiability 2x novelty because the hackathon judges value rigor over surprise").

Be decisive. Equal ranks are not allowed.
