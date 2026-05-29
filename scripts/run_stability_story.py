#!/usr/bin/env python3
"""Run one production stability sample through the optimized pipeline."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def run(cmd: List[str], env: Dict[str, str] | None = None) -> None:
    print("\n>>> " + " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=ROOT, env=env)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def run_json(cmd: List[str], env: Dict[str, str] | None = None) -> Dict[str, Any]:
    print("\n>>> " + " ".join(cmd), flush=True)
    completed = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n", flush=True)
    if completed.stderr:
        print(completed.stderr, end="" if completed.stderr.endswith("\n") else "\n", file=sys.stderr, flush=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {}


def story_path(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def scene_no_from_rel(path: str) -> int:
    match = re.search(r"scene-(\d+)\.md", path)
    return int(match.group(1)) if match else 1


def failed_scene_start(story: Path, run_id: str) -> int:
    report_path = story / "runs" / run_id / "split-scene-report.json"
    if not report_path.exists():
        return 1
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 1
    failed_numbers: List[int] = []
    for batch in report.get("batches", []):
        if batch.get("status") == "success":
            continue
        expected = batch.get("expected") or batch.get("written") or []
        failed_numbers.extend(scene_no_from_rel(str(item)) for item in expected)
    return min(failed_numbers) if failed_numbers else 1


def ensure_scene_generation(story: Path, model: str, effort: str, batch_size: int, timeout: int) -> None:
    env = os.environ.copy()
    env["STORYFORGE_CODEX_REASONING_EFFORT"] = effort
    primary_run = "split_scenes"
    cmd = [
        "python3",
        "scripts/generate_scene_batches.py",
        "--story",
        rel(story),
        "--batch-size",
        str(batch_size),
        "--model",
        model,
        "--effort",
        effort,
        "--timeout",
        str(timeout),
        "--retries",
        "3",
        "--force",
        "--run-id",
        primary_run,
    ]
    completed = subprocess.run(cmd, cwd=ROOT, env=env)
    if completed.returncode == 0:
        return

    start_at = failed_scene_start(story, primary_run)
    print(f"\nPrimary scene pass failed; retrying from scene {start_at} with batch size 1.", flush=True)
    run(
        [
            "python3",
            "scripts/generate_scene_batches.py",
            "--story",
            rel(story),
            "--batch-size",
            "1",
            "--model",
            model,
            "--effort",
            effort,
            "--timeout",
            str(timeout),
            "--retries",
            "4",
            "--start-at",
            str(start_at),
            "--run-id",
            "split_scenes_repair",
        ],
        env=env,
    )


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--model", default="gpt-5.4")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--rubric-threshold", type=float, default=8.0)
    args = parser.parse_args()

    story = story_path(args.story)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    env = os.environ.copy()
    env["STORYFORGE_CODEX_REASONING_EFFORT"] = args.effort

    run(
        [
            "python3",
            "scripts/storyforge.py",
            "run",
            "--story",
            rel(story),
            "--mode",
            "production",
            "--runner",
            "codex",
            "--model",
            args.model,
            "--to-phase",
            "4",
            "--max-retries",
            "1",
            "--no-human-gates",
            "--heartbeat-seconds",
            "60",
            "--run-id",
            f"phase1_4_{stamp}",
        ],
        env=env,
    )
    run(["python3", "scripts/production_normalize.py", "--story", rel(story), "--phase", "4", "--mode", "production"])
    run(["python3", "scripts/validate-production-story.py", "--story", rel(story), "--phase", "4", "--mode", "production", "--require-pass", "--json"])

    ensure_scene_generation(story, args.model, args.effort, args.batch_size, args.timeout)
    run(["python3", "scripts/repairs/repair_fragmentation_and_soft_words.py", "--story", rel(story)])
    run(["python3", "scripts/validate-production-story.py", "--story", rel(story), "--phase", "5", "--mode", "production", "--require-pass", "--json"])
    rhythm_draft = run_json(["python3", "scripts/rhythm_metrics.py", "--source", rel(story / "source.md"), "--candidate", rel(story / "draft.md"), "--json"])

    run(["python3", "scripts/write_machine_quality_report.py", "--story", rel(story), "--phase", "6", "--mode", "production"])
    run(["python3", "scripts/validate-production-story.py", "--story", rel(story), "--phase", "6", "--mode", "production", "--require-pass", "--json"])

    run(["python3", "scripts/package_from_draft_scenes.py", "--story", rel(story)])
    run(["python3", "scripts/write_machine_quality_report.py", "--story", rel(story), "--phase", "7", "--mode", "production"])
    run(["python3", "scripts/validate-production-story.py", "--story", rel(story), "--phase", "7", "--mode", "production", "--require-pass", "--json"])
    rhythm_final = run_json(["python3", "scripts/rhythm_metrics.py", "--source", rel(story / "source.md"), "--candidate", rel(story / "final.md"), "--json"])
    rubric = run_json(
        [
            "python3",
            "scripts/tomato-rubric-score.py",
            "--story",
            rel(story),
            "--threshold",
            str(args.rubric_threshold),
            "--write-report",
            "--json",
        ]
    )
    hook_score = (
        ((rubric.get("dimensions") or {}).get("hook_density") or {}).get("score")
        if isinstance(rubric, dict)
        else None
    )
    if hook_score is not None and float(hook_score) < 8.0:
        raise SystemExit(f"hook_density hard gate failed: {hook_score}")

    report = {
        "story": rel(story),
        "status": "pass",
        "draft_rhythm": rhythm_draft,
        "final_rhythm": rhythm_final,
        "rubric": rubric,
        "quality": read_json(story / "quality-report.json"),
    }
    out = story / "stability-story-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"story": rel(story), "status": "pass", "report": rel(out)}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
