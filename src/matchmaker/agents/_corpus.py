"""Shared helpers for compacting a ResearcherProfile into prompt-ready text."""

from __future__ import annotations

from matchmaker.schemas import ResearcherProfile


def format_publications_block(
    profile: ResearcherProfile,
    *,
    max_chars_per_pub: int = 2500,
) -> str:
    """Render the profile as a labeled markdown block usable in any prompt.

    Each publication appears with its stable Publication.id, title, and a
    truncated body so agents can cite it back via `evidence` fields.
    """
    parts: list[str] = []
    for pub in profile.publications:
        body = (pub.full_text_md or pub.abstract or "").strip()
        if len(body) > max_chars_per_pub:
            body = body[:max_chars_per_pub].rsplit(" ", 1)[0] + " ..."
        parts.append(
            f"## [{pub.id}] {pub.title}\n\n{body}\n"
        )
    return "\n".join(parts)
