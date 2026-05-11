"""Stage 5 — load ResearcherPrompt from prompts_input/<id>.md.

Convention (case-insensitive):
    ## Current focus
    Free text.

    ## Recent milestones
    - bullet
    - bullet

    ## Blockers
    - bullet

    ## Notes        (optional, free text -> free_text)

Missing sections become empty/None. Extra sections under unknown headings are
absorbed into free_text so authors can't lose content by mistyping a heading.
"""

from __future__ import annotations

import re
from pathlib import Path

from matchmaker.logging import get_logger
from matchmaker.schemas import ResearcherPrompt

log = get_logger(__name__)


_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_BULLET = re.compile(r"^[\-*]\s+(.+?)\s*$", re.MULTILINE)


def _split_sections(text: str) -> dict[str, str]:
    """Return {lowered_heading: body} for every ## section in the file."""
    matches = list(_HEADING.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end].strip()
        out[m.group(1).strip().lower()] = body
    return out


def _bullets(body: str) -> list[str]:
    return [m.group(1).strip() for m in _BULLET.finditer(body)]


_KNOWN = {"current focus", "recent milestones", "blockers", "notes"}


def parse_prompt_markdown(text: str, *, researcher_id: str) -> ResearcherPrompt:
    sections = _split_sections(text)

    current_focus = sections.get("current focus", "").strip()
    if not current_focus:
        raise ValueError(
            f"Prompt for {researcher_id!r} missing required '## Current focus' section."
        )

    milestones = _bullets(sections.get("recent milestones", ""))
    blockers = _bullets(sections.get("blockers", ""))

    extra_parts: list[str] = []
    notes_body = sections.get("notes", "").strip()
    if notes_body:
        extra_parts.append(notes_body)
    for heading, body in sections.items():
        if heading not in _KNOWN and body.strip():
            extra_parts.append(f"### {heading}\n{body.strip()}")
    free_text = "\n\n".join(extra_parts) if extra_parts else None

    return ResearcherPrompt(
        researcher_id=researcher_id,
        current_focus=current_focus,
        recent_milestones=milestones,
        blockers=blockers,
        free_text=free_text,
    )


def load_researcher_prompt(prompts_dir: Path, researcher_id: str) -> ResearcherPrompt:
    path = prompts_dir / f"{researcher_id}.md"
    if not path.is_file():
        raise FileNotFoundError(
            f"No prompt file for {researcher_id!r} at {path}. "
            f"Author it with at least a '## Current focus' section."
        )
    text = path.read_text(encoding="utf-8")
    prompt = parse_prompt_markdown(text, researcher_id=researcher_id)
    log.info(
        "ingestion.prompts.loaded",
        researcher_id=researcher_id,
        path=str(path),
        n_milestones=len(prompt.recent_milestones),
        n_blockers=len(prompt.blockers),
    )
    return prompt
