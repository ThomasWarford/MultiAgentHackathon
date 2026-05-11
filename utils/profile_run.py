"""Run the matchmaker pipeline once, then plot per-stage time and cost.

Parses the run's structured log to attribute every `llm.call.done` event to
the most recently started node (`node.<stage>.start`). Stage duration is the
gap between consecutive `node.*.start` events, with the last stage ending at
`run.done`.

Outputs:
  outputs/profile/<run_id>_time.png
  outputs/profile/<run_id>_cost.png
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]

TS_RE = re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+\[\w+\s*\]\s+(?P<event>\S+)\s*(?P<rest>.*)$")
KV_RE = re.compile(r"(\w+)=([^\s]+)")

STAGE_ORDER = [
    "ingest",
    "background",
    "extract",
    "cross_factorial",
    "load_prompts",
    "hypotheses",
    "refine_loop",
    "rank",
]


def parse_ts(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)


def parse_log(log_path: Path) -> tuple[dict[str, float], dict[str, float], str]:
    """Return (durations_s, costs_usd, run_id) keyed by stage name."""
    stage_starts: list[tuple[str, datetime]] = []
    stage_costs: dict[str, float] = {s: 0.0 for s in STAGE_ORDER}
    run_done_ts: datetime | None = None
    run_id = "unknown"
    current_stage: str | None = None

    for raw in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = TS_RE.match(raw.strip())
        if not m:
            continue
        ts = parse_ts(m.group("ts"))
        event = m.group("event")
        kv = dict(KV_RE.findall(m.group("rest")))

        if event.startswith("node.") and event.endswith(".start"):
            stage = event[len("node.") : -len(".start")]
            stage_starts.append((stage, ts))
            current_stage = stage
            if "run_id" in kv and run_id == "unknown":
                run_id = kv["run_id"]

        elif event == "llm.call.done" and current_stage is not None:
            try:
                delta = float(kv.get("delta_usd", "0"))
            except ValueError:
                delta = 0.0
            stage_costs[current_stage] = stage_costs.get(current_stage, 0.0) + delta

        elif event == "run.done":
            run_done_ts = ts

    durations: dict[str, float] = {}
    for i, (stage, start_ts) in enumerate(stage_starts):
        end_ts = stage_starts[i + 1][1] if i + 1 < len(stage_starts) else run_done_ts
        if end_ts is None:
            continue
        durations[stage] = (end_ts - start_ts).total_seconds()

    return durations, stage_costs, run_id


def plot_bars(
    title: str,
    ylabel: str,
    data: dict[str, float],
    total_label: str,
    out_path: Path,
    color: str,
    value_fmt: str,
) -> None:
    stages = [s for s in STAGE_ORDER if s in data]
    values = [data[s] for s in stages]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(stages, values, color=color, edgecolor="black", linewidth=0.5)
    ax.set_title(f"{title}\n{total_label}")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Pipeline stage")
    ax.tick_params(axis="x", rotation=30)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            value_fmt.format(val),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.margins(y=0.15)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> int:
    run_id = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    log_path = ROOT / "outputs" / "profile" / f"{run_id}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[profile] running pipeline run_id={run_id}", flush=True)
    with log_path.open("w", encoding="utf-8") as log_f:
        proc = subprocess.run(
            [
                "uv", "run", "matchmaker", "run",
                "--a", "csanyi",
                "--b", "pellegrini",
                "--run-id", run_id,
            ],
            cwd=ROOT,
            stdout=log_f,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if proc.returncode != 0:
        print(f"[profile] pipeline exited with code {proc.returncode}; log: {log_path}", file=sys.stderr)
        return proc.returncode

    durations, costs, parsed_run_id = parse_log(log_path)
    total_time = sum(durations.values())
    total_cost = sum(costs.values())

    print(f"[profile] run_id={parsed_run_id}")
    print(f"[profile] total time:  {total_time:.2f} s")
    print(f"[profile] total cost: ${total_cost:.4f}")
    print("[profile] per stage:")
    for stage in STAGE_ORDER:
        if stage in durations:
            print(f"  {stage:<16} {durations[stage]:7.2f} s   ${costs.get(stage, 0.0):.4f}")

    time_png = log_path.parent / f"{run_id}_time.png"
    cost_png = log_path.parent / f"{run_id}_cost.png"
    plot_bars(
        title="Matchmaker pipeline — time per stage",
        ylabel="Duration (s)",
        data=durations,
        total_label=f"Total: {total_time:.2f} s",
        out_path=time_png,
        color="#4C72B0",
        value_fmt="{:.1f}s",
    )
    plot_bars(
        title="Matchmaker pipeline — cost per stage",
        ylabel="Cost (USD)",
        data=costs,
        total_label=f"Total: ${total_cost:.4f}",
        out_path=cost_png,
        color="#55A868",
        value_fmt="${:.4f}",
    )
    print(f"[profile] wrote {time_png}")
    print(f"[profile] wrote {cost_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
