"""Artifact writer tests."""

from __future__ import annotations

import json
from pathlib import Path

from matchmaker.io.artifacts import write_artifact
from matchmaker.schemas import Publication, ResearcherProfile


def test_writes_timestamped_file(tmp_path: Path) -> None:
    profile = ResearcherProfile(
        researcher_id="x",
        display_name="X",
        publications=[Publication(id="p1", title="T", source="local", source_id="x.md")],
    )
    path = write_artifact(tmp_path, "01_publications", "runA", profile)
    assert path.exists()
    assert path.suffix == ".json"
    body = json.loads(path.read_text(encoding="utf-8"))
    assert body["stage"] == "01_publications"
    assert body["run_id"] == "runA"
    assert "timestamp_utc" in body
    assert body["payload"]["researcher_id"] == "x"


def test_dict_of_models_serializes(tmp_path: Path) -> None:
    profile = ResearcherProfile(
        researcher_id="x",
        display_name="X",
        publications=[Publication(id="p1", title="T", source="local", source_id="x.md")],
    )
    path = write_artifact(
        tmp_path,
        "01_publications",
        "runB",
        {"profile_a": profile, "profile_b": None},
    )
    body = json.loads(path.read_text(encoding="utf-8"))
    assert body["payload"]["profile_a"]["researcher_id"] == "x"
    assert body["payload"]["profile_b"] is None


def test_two_writes_dont_overwrite(tmp_path: Path) -> None:
    profile = ResearcherProfile(
        researcher_id="x",
        display_name="X",
        publications=[Publication(id="p1", title="T", source="local", source_id="x.md")],
    )
    # write_artifact stamps with seconds precision; force two distinct names.
    import time
    p1 = write_artifact(tmp_path, "stage", "r1", profile)
    time.sleep(1.1)
    p2 = write_artifact(tmp_path, "stage", "r2", profile)
    assert p1 != p2
    assert p1.exists() and p2.exists()
