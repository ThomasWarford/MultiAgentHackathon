You are revising a collaborative research hypothesis in response to a reviewer's critique.

# Hypothesis (current version)
- ID: {hypothesis_id}
- Title: {title}
- Statement: {statement}
- Mechanism: {mechanism}
- Leverages cells: {leverages_str}
- Addresses prompts: {addresses_str}
- Self-reported confidence: {confidence:.2f}

# Latest critique (iteration {iteration})
- Severity: {severity}
- Strengths: {strengths_block}
- Weaknesses: {weaknesses_block}
- Suggested revisions: {revisions_block}

# Prior critique iterations (oldest first)
{history_block}

# Your task
Produce a refined hypothesis that substantively addresses the critique. You may:
- Tighten the statement to make it more falsifiable.
- Add specificity to the mechanism (which dataset, which experiment, which deliverable).
- Adjust leverages or addresses_prompts if the revision changes scope.
- Update confidence to reflect the post-revision state.

Do NOT:
- Repeat a revision that was already attempted in a prior iteration (visible in history).
- Drop the core idea — refine, don't replace.

In `revision_notes`, briefly list what changed and why. Keep `hypothesis_id` stable.
