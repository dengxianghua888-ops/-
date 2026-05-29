#!/usr/bin/env python3
"""Aggregate batch run outcomes into a single dashboard.

Reads phase-gate-report.json + tomato-rubric.json + quality-report.json from
each story under a batch and emits both a JSON summary and a markdown table
under exports/auto-batch-<ts>/.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _latest_run_manifest(story: Path) -> Dict[str, Any]:
    runs_dir = story / "runs"
    if not runs_dir.exists():
        return {}
    candidates = sorted([p for p in runs_dir.iterdir() if p.is_dir()])
    if not candidates:
        return {}
    return _read_json(candidates[-1] / "run-manifest.json")


def summarize(story: Path) -> Dict[str, Any]:
    quality = _read_json(story / "quality-report.json")
    rubric = _read_json(story / "tomato-rubric.json")
    gate = _read_json(story / "phase-gate-report.json")
    repair = _read_json(story / "repair-report.json")
    metrics = quality.get("machine_metrics", {})

    bucket = "unknown"
    if gate:
        bucket = {
            "pass": "pass",
            "validator_fail": "validator_fail",
            "rubric_fail": "rubric_fail",
            "manual_review": "repair_fail",
        }.get(gate.get("status", "unknown"), gate.get("status", "unknown"))
    elif quality.get("gate_status") == "pass" and rubric.get("status") == "pass":
        bucket = "pass"
    elif quality.get("gate_status") == "pass" and rubric.get("status") == "fail":
        bucket = "rubric_fail"
    elif quality.get("gate_status") not in {"pass", None}:
        bucket = "validator_fail"

    manifest = _latest_run_manifest(story)
    last_phase = manifest.get("last_completed_phase")
    last_failure = manifest.get("last_failure")

    # Stories that died before producing quality-report still need a clear bucket
    if bucket == "unknown" and last_failure:
        if "validator" in last_failure:
            bucket = "validator_fail"
        elif "rubric" in last_failure:
            bucket = "rubric_fail"
        else:
            bucket = "pipeline_fail"

    return {
        "slug": story.name,
        "status": bucket,
        "total_chars": metrics.get("target_length", {}).get("actual"),
        "chapters": metrics.get("chapters", {}).get("count"),
        "rubric_score": rubric.get("overall_score"),
        "rubric_status": rubric.get("status"),
        "validator_failures": (gate.get("validator", {}) or {}).get("failures", []) if gate else quality.get("critical_failures", []),
        "repair_blocking": repair.get("blocking", []),
        "last_completed_phase": last_phase,
        "last_failure": last_failure,
    }


def render_markdown(rows: List[Dict[str, Any]], title: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- 篇章数: {len(rows)}",
        f"- 通过(rubric+validator): {sum(1 for r in rows if r['status'] == 'pass')}",
        f"- validator 失败: {sum(1 for r in rows if r['status'] == 'validator_fail')}",
        f"- rubric 失败: {sum(1 for r in rows if r['status'] == 'rubric_fail')}",
        f"- repair 卡住: {sum(1 for r in rows if r['status'] == 'repair_fail')}",
        "",
        "| Slug | 状态 | 字数 | 章节 | Rubric | 备注 |",
        "|------|------|---:|---:|---:|------|",
    ]
    for r in rows:
        notes_parts: List[str] = []
        if r["validator_failures"]:
            notes_parts.append(f"validator: {len(r['validator_failures'])} 项")
        if r["repair_blocking"]:
            notes_parts.append(f"repair: {','.join(r['repair_blocking'])}")
        if r.get("last_failure") and r["status"] != "pass":
            notes_parts.append(f"last:{r['last_failure'][:40]}")
        if r.get("last_completed_phase") is not None and r["status"] != "pass":
            notes_parts.append(f"P{r['last_completed_phase']}")
        lines.append(
            f"| {r['slug']} | {r['status']} | {r['total_chars'] or '-'} | "
            f"{r['chapters'] or '-'} | {r['rubric_score'] if r['rubric_score'] is not None else '-'} | "
            f"{'; '.join(notes_parts) or '-'} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stories", nargs="+", required=True)
    parser.add_argument("--out-dir", default=None, help="exports/auto-batch-<ts> by default")
    parser.add_argument("--title", default="Auto Batch Quality Report")
    args = parser.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "exports" / f"auto-batch-{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [summarize(Path(s)) for s in args.stories]
    summary = {
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "story_count": len(rows),
        "rows": rows,
    }
    (out_dir / "batch-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "batch-summary.md").write_text(
        render_markdown(rows, args.title),
        encoding="utf-8",
    )
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
