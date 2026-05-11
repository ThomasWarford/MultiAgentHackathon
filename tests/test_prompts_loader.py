"""ResearcherPrompt parser tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from matchmaker.ingestion import load_researcher_prompt, parse_prompt_markdown


def test_full_parse() -> None:
    md = """## Current focus
Studying liquid water at coupled-cluster accuracy.

## Recent milestones
- Trained MLIP on 100k structures
- Submitted JCP paper

## Blockers
- DFT noise in training data
- Computational budget for evaluation

## Notes
Extra context goes here.
"""
    p = parse_prompt_markdown(md, researcher_id="csanyi")
    assert p.researcher_id == "csanyi"
    assert "coupled-cluster" in p.current_focus
    assert p.recent_milestones == ["Trained MLIP on 100k structures", "Submitted JCP paper"]
    assert p.blockers == [
        "DFT noise in training data",
        "Computational budget for evaluation",
    ]
    assert p.free_text == "Extra context goes here."


def test_missing_current_focus_raises() -> None:
    md = "## Blockers\n- something\n"
    with pytest.raises(ValueError, match="Current focus"):
        parse_prompt_markdown(md, researcher_id="x")


def test_unknown_sections_absorbed_into_free_text() -> None:
    md = """## Current focus
Some focus.

## Random Heading
Some content that would otherwise be lost.
"""
    p = parse_prompt_markdown(md, researcher_id="x")
    assert "Some content that would otherwise be lost" in (p.free_text or "")


def test_case_insensitive_headings() -> None:
    md = "## CURRENT FOCUS\nx.\n\n## blockers\n- y\n"
    p = parse_prompt_markdown(md, researcher_id="x")
    assert p.current_focus == "x."
    assert p.blockers == ["y"]


def test_load_from_disk(tmp_path: Path) -> None:
    (tmp_path / "alice.md").write_text(
        "## Current focus\nDoing things.\n",
        encoding="utf-8",
    )
    p = load_researcher_prompt(tmp_path, "alice")
    assert p.researcher_id == "alice"
    assert p.current_focus == "Doing things."


def test_load_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_researcher_prompt(tmp_path, "nobody")
