"""LocalCorpusSource invariants + a real-corpus sanity check."""

from __future__ import annotations

from pathlib import Path

import pytest

from matchmaker.ingestion import LocalCorpusSource
from matchmaker.ingestion.local_corpus import _extract_title

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = REPO_ROOT / "papers"


class TestTitleExtraction:
    def test_h1_wins(self) -> None:
        md = "## RESEARCH ARTICLE\n\n# The Real Title Of The Paper\n\nbody"
        assert _extract_title(md, "fallback") == "The Real Title Of The Paper"

    def test_bold_h2_when_no_h1(self) -> None:
        md = "## **A Bolded H2 Title Of Sufficient Length**\n\nbody"
        assert _extract_title(md, "fallback") == "A Bolded H2 Title Of Sufficient Length"

    def test_skips_venue_metadata(self) -> None:
        md = "## **Article**\n\n# Actual Title Of The Paper\n"
        assert _extract_title(md, "fallback") == "Actual Title Of The Paper"

    def test_falls_back_when_no_heading(self) -> None:
        md = "no headings here, just prose"
        assert _extract_title(md, "fallback-title") == "fallback-title"


class TestLocalCorpusSource:
    async def test_missing_researcher_dir_raises(self, tmp_path: Path) -> None:
        src = LocalCorpusSource(tmp_path)
        with pytest.raises(FileNotFoundError):
            await src.fetch("nobody")

    async def test_empty_researcher_dir_raises(self, tmp_path: Path) -> None:
        (tmp_path / "x").mkdir()
        src = LocalCorpusSource(tmp_path)
        with pytest.raises(FileNotFoundError):
            await src.fetch("x")

    async def test_tmp_corpus_round_trip(self, tmp_path: Path) -> None:
        d = tmp_path / "alice"
        d.mkdir()
        (d / "paper1.md").write_text("# A Paper About Things\n\nbody.", encoding="utf-8")
        (d / "paper2.md").write_text(
            "## **Another Paper Of Sufficient Length**\n\nbody.", encoding="utf-8"
        )
        src = LocalCorpusSource(tmp_path)
        profile = await src.fetch("alice")
        assert profile.researcher_id == "alice"
        assert len(profile.publications) == 2
        # IDs must be stable across runs for the same (researcher, filename).
        ids = {p.id for p in profile.publications}
        again = await src.fetch("alice")
        assert {p.id for p in again.publications} == ids


@pytest.mark.skipif(not PAPERS_DIR.exists(), reason="papers/ corpus not present")
class TestRealCorpus:
    async def test_csanyi_loads(self) -> None:
        src = LocalCorpusSource(PAPERS_DIR)
        profile = await src.fetch("csanyi")
        assert profile.display_name == "Gábor Csányi"
        assert len(profile.publications) >= 8
        for p in profile.publications:
            assert p.title and len(p.title) >= 8
            assert p.full_text_md and len(p.full_text_md) > 1000

    async def test_pellegrini_loads(self) -> None:
        src = LocalCorpusSource(PAPERS_DIR)
        profile = await src.fetch("pellegrini")
        assert profile.display_name == "Adam F. A. Pellegrini"
        assert len(profile.publications) >= 8
