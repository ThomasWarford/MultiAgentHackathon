"""LocalCorpusSource — reads pre-converted markdown from papers/<researcher>/.

This is the MVP default. Each .md file under papers/<researcher_id>/ becomes
one Publication; the title is extracted from the first H1 (or bolded H2) the
parser finds, falling back to a humanized filename. Author, year, and DOI are
left to downstream agents that can pull them from full_text_md if needed.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from matchmaker.ingestion.source import Source
from matchmaker.logging import get_logger
from matchmaker.schemas import Publication, ResearcherProfile

log = get_logger(__name__)


# Optional human-readable name overrides; falls back to title-cased researcher_id.
_DISPLAY_NAMES: dict[str, str] = {
    "csanyi": "Gábor Csányi",
    "pellegrini": "Adam F. A. Pellegrini",
}


_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_BOLD_H2 = re.compile(r"^##\s+\*\*(.+?)\*\*\s*$", re.MULTILINE)
_FORMATTING = re.compile(r"[*_~`]+")


def _extract_title(markdown: str, fallback: str) -> str:
    for pattern in (_H1, _BOLD_H2):
        for match in pattern.finditer(markdown):
            candidate = _FORMATTING.sub("", match.group(1)).strip()
            # Skip obvious venue/section metadata.
            lowered = candidate.lower()
            if any(
                lowered.startswith(prefix)
                for prefix in (
                    "research article",
                    "article",
                    "articles you may",
                    "abstract",
                    "introduction",
                    "i.",
                    "ii.",
                )
            ):
                continue
            if len(candidate) < 8:
                continue
            return candidate
    return fallback


def _stable_id(researcher_id: str, filename: str) -> str:
    h = hashlib.sha1(f"{researcher_id}:{filename}".encode("utf-8")).hexdigest()[:12]
    return f"{researcher_id}_{h}"


def _humanize_filename(stem: str) -> str:
    cleaned = re.sub(r"[_\-]+", " ", stem).strip()
    return cleaned[:120]


class LocalCorpusSource(Source):
    def __init__(self, papers_dir: Path) -> None:
        self._papers_dir = papers_dir

    async def fetch(self, researcher_id: str) -> ResearcherProfile:
        researcher_dir = self._papers_dir / researcher_id
        if not researcher_dir.is_dir():
            raise FileNotFoundError(
                f"No papers directory for {researcher_id!r} at {researcher_dir}."
            )

        publications: list[Publication] = []
        for md_path in sorted(researcher_dir.glob("*.md")):
            text = md_path.read_text(encoding="utf-8")
            title = _extract_title(text, fallback=_humanize_filename(md_path.stem))
            publications.append(
                Publication(
                    id=_stable_id(researcher_id, md_path.name),
                    title=title,
                    source="local",
                    source_id=md_path.name,
                    full_text_md=text,
                )
            )

        if not publications:
            raise FileNotFoundError(f"No .md files in {researcher_dir}.")

        profile = ResearcherProfile(
            researcher_id=researcher_id,
            display_name=_DISPLAY_NAMES.get(researcher_id, researcher_id.title()),
            publications=publications,
        )

        log.info(
            "ingestion.local.loaded",
            researcher_id=researcher_id,
            n_publications=len(publications),
            source_dir=str(researcher_dir),
        )
        return profile
