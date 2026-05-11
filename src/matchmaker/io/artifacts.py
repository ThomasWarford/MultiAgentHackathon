"""Per-stage artifact writer.

Files are timestamped + run-id-suffixed under outputs/<stage>/; never
overwritten so two consecutive runs both leave their record on disk and you
can diff them.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def _to_jsonable(payload: Any) -> Any:
    if isinstance(payload, BaseModel):
        return payload.model_dump(mode="json")
    if isinstance(payload, dict):
        return {k: _to_jsonable(v) for k, v in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [_to_jsonable(x) for x in payload]
    return payload


def write_artifact(
    outputs_dir: Path,
    stage: str,
    run_id: str,
    payload: Any,
) -> Path:
    stage_dir = outputs_dir / stage
    stage_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = stage_dir / f"{ts}_{run_id}.json"

    body = {
        "stage": stage,
        "run_id": run_id,
        "timestamp_utc": ts,
        "payload": _to_jsonable(payload),
    }
    path.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
