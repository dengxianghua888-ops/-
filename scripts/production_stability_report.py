#!/usr/bin/env python3
"""Summarize StoryForge production runs across one or more stories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_summary(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    phases: List[Dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|") or line.startswith("|---") or "Phase" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 9 or not cells[0].isdigit():
            continue
        phases.append(
            {
                "phase": int(cells[0]),
                "status": cells[1],
                "started": cells[2],
                "ended": cells[3],
                "duration": cells[4],
                "retries": cells[5],
                "runner": cells[6],
                "provider": cells[7],
                "notes": cells[8],
            }
        )
    return phases


def validator_failures(path: Path) -> List[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict) and isinstance(payload.get("failures"), list):
        return [str(item) for item in payload["failures"]]
    failures = []
    for match in re.finditer(r'"failures"\s*:\s*\[(.*?)\]', text, flags=re.DOTALL):
        failures.extend(item.strip().strip('"') for item in match.group(1).split(",") if item.strip())
    if failures:
        return failures
    return [line.strip() for line in text.splitlines() if "fail" in line.lower()]


def phase_log_details(run_dir: Path, phase: Dict[str, Any]) -> Dict[str, Any]:
    number = int(phase["phase"])
    normalizer_path = run_dir / f"phase{number}.normalizer.log"
    normalizer: Dict[str, Any] = {}
    if normalizer_path.exists():
        try:
            normalizer = load_json(normalizer_path)
        except json.JSONDecodeError:
            normalizer = {"error": normalizer_path.read_text(encoding="utf-8")}
    enriched = dict(phase)
    enriched["normalizer_changes"] = normalizer.get("changes", []) if isinstance(normalizer, dict) else []
    enriched["validator_failures"] = validator_failures(run_dir / f"phase{number}.validator.log")
    return enriched


def final_metrics(story: Path) -> Dict[str, Any]:
    report_path = story / "quality-report.json"
    if not report_path.exists():
        return {}
    try:
        report = load_json(report_path)
    except json.JSONDecodeError:
        return {}
    return report.get("machine_metrics", {}) if isinstance(report.get("machine_metrics"), dict) else {}


def collect_story(story: Path) -> Dict[str, Any]:
    runs = []
    for run_dir in sorted((story / "runs").glob("*")):
        if not run_dir.is_dir():
            continue
        phases = [phase_log_details(run_dir, phase) for phase in parse_summary(run_dir / "execution-summary.md")]
        manifest = {}
        manifest_path = run_dir / "run-manifest.json"
        if manifest_path.exists():
            try:
                manifest = load_json(manifest_path)
            except json.JSONDecodeError:
                manifest = {}
        runs.append(
            {
                "run_id": run_dir.name,
                "path": str(run_dir),
                "status": manifest.get("status", "unknown"),
                "started_at": manifest.get("started_at", ""),
                "ended_at": manifest.get("ended_at", ""),
                "phases": phases,
            }
        )
    return {"story": str(story), "runs": runs, "final_machine_metrics": final_metrics(story)}


def render_markdown(payload: Dict[str, Any]) -> str:
    lines = ["# StoryForge Production Stability Report", ""]
    for story in payload["stories"]:
        lines.extend([f"## {story['story']}", ""])
        if not story["runs"]:
            lines.extend(["No runs found.", ""])
            continue
        for run in story["runs"]:
            lines.extend(
                [
                    f"### Run `{run['run_id']}`",
                    "",
                    f"- Status: {run['status']}",
                    f"- Started: {run['started_at'] or '-'}",
                    f"- Ended: {run['ended_at'] or '-'}",
                    "",
                    "| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |",
                    "|---:|---|---:|---|---|---|---|---|",
                ]
            )
            for phase in run["phases"]:
                changes = ", ".join(phase.get("normalizer_changes", [])) or "-"
                failures = "; ".join(phase.get("validator_failures", [])[:3]) or "-"
                lines.append(
                    f"| {phase['phase']} | {phase['status']} | {phase['duration']} | "
                    f"{phase['runner']} | {phase['provider']} | {changes} | {failures} | {phase['notes']} |"
                )
            lines.append("")
        metrics = story.get("final_machine_metrics") or {}
        if metrics:
            failures = "; ".join(metrics.get("failures", [])) if isinstance(metrics.get("failures"), list) else ""
            target = metrics.get("target_length", {}) if isinstance(metrics.get("target_length"), dict) else {}
            chapters = metrics.get("chapters", {}) if isinstance(metrics.get("chapters"), dict) else {}
            lines.extend(
                [
                    "Final Phase 8 Metrics:",
                    "",
                    f"- Target length actual: {target.get('actual', '-')}",
                    f"- Chapter count: {chapters.get('count', '-')}",
                    f"- Chapter hook coverage: {chapters.get('hook_coverage', '-')}",
                    f"- Failures: {failures or '-'}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(out: Path, payload: Dict[str, Any]) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(payload), encoding="utf-8")
    json_path = out.with_suffix(".json")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stories", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = {"stories": [collect_story(Path(story)) for story in args.stories]}
    write_outputs(Path(args.out), payload)
    print(json.dumps({"out": args.out, "json": str(Path(args.out).with_suffix(".json"))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
