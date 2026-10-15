#!/usr/bin/env python3
"""StoryForge V4 automation state machine."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from storyforge_lib import (
    apply_artifact_bundle,
    load_phase_bundle,
    normalize_pipeline_mode,
    now_run_id,
    now_stamp,
    phase_count,
    phase_key,
    phase_for_role,
    StagedStory,
    story_write_lock,
    render_phase_prompt,
    repo_root,
    validate_bundle_schema,
    write_json,
    write_text,
)
from production_normalize import normalize_story


ROOT = repo_root()
RUNNER_EXIT_RUNNER_FAILED = 20


def _load_rubric_config() -> Dict[str, Any]:
    """Read tomato_rubric block from workspace.yaml; return defaults on any error."""
    defaults = {"enabled": True, "pass_threshold": 8.0}
    try:
        import yaml  # type: ignore
        ws = yaml.safe_load((ROOT / "workspace.yaml").read_text(encoding="utf-8")) or {}
        cfg = (((ws.get("pipeline") or {}).get("quality_gate") or {}).get("tomato_rubric") or {})
        return {**defaults, **cfg}
    except Exception:
        return defaults


RUBRIC_CONFIG = _load_rubric_config()
RUNNER_EXIT_PARSE_FAILED = 21
RUNNER_EXIT_VALIDATION_FAILED = 23
RUNNER_EXIT_HUMAN_GATE = 24


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def run_command(args: List[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def _append_progress(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def run_command_with_heartbeat(
    args: List[str],
    run_dir: Path,
    phase: int,
    provider_hint: str,
    heartbeat_seconds: float,
    cwd: Path = ROOT,
) -> tuple[subprocess.CompletedProcess[str], Dict[str, Any]]:
    started_at = now_stamp()
    started = time.time()
    proc = subprocess.Popen(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress = run_dir / f"phase{phase}.runner.progress.log"

    def emit(status: str) -> None:
        elapsed = round(time.time() - started, 3)
        line = (
            f"phase={phase} elapsed={elapsed}s pid={proc.pid} provider={provider_hint or '-'} "
            f"run_dir={run_dir} status={status}"
        )
        _append_progress(progress, line)
        eprint(line)

    emit("started")
    timeout_value = heartbeat_seconds if heartbeat_seconds and heartbeat_seconds > 0 else None
    if timeout_value is None:
        stdout, stderr = proc.communicate()
    else:
        while True:
            try:
                stdout, stderr = proc.communicate(timeout=timeout_value)
                break
            except subprocess.TimeoutExpired:
                emit("running")
    ended_at = now_stamp()
    emit(f"exited:{proc.returncode}")
    completed = subprocess.CompletedProcess(args, proc.returncode, stdout or "", stderr or "")
    metadata = {
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_s": round(time.time() - started, 3),
        "timeout": False,
        "pid": proc.pid,
        "progress_log": str(progress),
    }
    return completed, metadata


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def command_for_runner(runner: str) -> List[str]:
    script_map = {
        "agent": "agent-runner.py",
        "codex": "agent-runner.py",
        "openclaw": "agent-runner.py",
        "claude": "agent-runner.py",
        "mock": "mock-runner.py",
        "manual-prompt-pack": "manual-prompt-pack-runner.py",
        "local-ollama": "local-ollama-runner.py",
    }
    if runner not in script_map:
        raise ValueError(f"unknown runner: {runner}")
    return [sys.executable, str(ROOT / "scripts" / "runners" / script_map[runner])]


def runner_args(runner: str, story: Path, phase: int, prompt: Path, run_dir: Path, model: str, mode: str) -> List[str]:
    args = command_for_runner(runner)
    args.extend([
        "--story",
        str(story),
        "--phase",
        str(phase),
        "--prompt",
        str(prompt),
        "--run-dir",
        str(run_dir),
    ])
    if model:
        args.extend(["--model", model])
    if runner in {"agent", "codex", "openclaw", "claude", "mock", "manual-prompt-pack"}:
        args.extend(["--mode", mode])
    if runner in {"codex", "openclaw", "claude"}:
        args.extend(["--providers", runner])
    return args


def init_summary(story: Path, run_dir: Path, run_id: str, runner: str, from_phase: int, max_retries: int) -> Path:
    summary = run_dir / "execution-summary.md"
    if summary.exists():
        return summary
    write_text(
        summary,
        "\n".join(
            [
                f"# Execution Summary — {story}",
                "",
                f"- **Run ID**: {run_id}",
                f"- **Story**: {story}",
                f"- **Start**: {now_stamp()}",
                f"- **Runner**: {runner}",
                f"- **Start Phase**: {from_phase}",
                f"- **Max Retries**: {max_retries}",
                "",
                "## Phase Log",
                "",
                "| Phase | Status | Started | Ended | Duration | Retries | Runner | Provider | Notes |",
                "|-------|--------|---------|-------|----------|---------|--------|----------|-------|",
            ]
        )
        + "\n",
    )
    return summary


def append_summary(summary: Path, phase: int, status: str, started: str, duration_s: int, retry: int, runner: str, provider: str, notes: str) -> None:
    with summary.open("a", encoding="utf-8") as handle:
        handle.write(
            f"| {phase} | {status} | {started} | {now_stamp()} | {duration_s}s | "
            f"{retry} | {runner} | {provider or '-'} | {notes} |\n"
        )


def update_manifest(run_dir: Path, patch: Dict[str, Any]) -> None:
    path = run_dir / "run-manifest.json"
    data: Dict[str, Any] = {}
    if path.exists():
        data = load_json(path)
    data.update(patch)
    data["updated_at"] = now_stamp()
    write_json(path, data)


def strip_top_sections(text: str, section_names: set[str]) -> str:
    lines = text.splitlines()
    kept: List[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith((" ", "\t")) and ":" in line:
            key = line.split(":", 1)[0].strip()
            if key in section_names:
                index += 1
                while index < len(lines):
                    child = lines[index]
                    if child.strip() and not child.startswith((" ", "\t")) and ":" in child:
                        break
                    index += 1
                continue
        kept.append(line)
        index += 1
    return "\n".join(kept).rstrip() + "\n"


def update_story_automation(story: Path, patch: Dict[str, Any]) -> None:
    path = story / "story.yaml"
    # Automation updates never grant source access or erase unrelated metadata.
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    data = data or {"slug": story.name, "status": "phase1", "current_phase": 1}
    automation = data.setdefault("automation", {})
    for key, value in patch.items():
        if key == "phase2_blueprint_review":
            automation.setdefault("human_gates", {})[key] = value
        else:
            automation[key] = value
    write_text(path, yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def story_source_access(story: Path) -> str:
    manifest = story / "story.yaml"
    if not manifest.exists():
        return "trusted_runners_allowed"
    import yaml
    try:
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        if data.get("source_policy", {}).get("access") == "denied":
            return "denied"
    except (yaml.YAMLError, AttributeError):
        return "denied"
    return "trusted_runners_allowed"


def re_search_denied(text: str) -> bool:
    import re

    section = re.search(r"^source_policy:\s*\n(.*?)(?=^\S|\Z)", text, re.MULTILINE | re.DOTALL)
    return bool(section and re.search(r"^\s*access:\s*denied\s*$", section.group(1), re.MULTILINE))


def validate_phase(story: Path, phase: int, require_pass: bool = False, mode: str = "v4") -> subprocess.CompletedProcess[str]:
    normalized = normalize_pipeline_mode(mode)
    if normalized in {"production", "production_v6", "ultra_short"}:
        args = [
            sys.executable,
            str(ROOT / "scripts" / "validate-production-story.py"),
            "--story",
            str(story),
            "--phase",
            str(phase),
            "--mode",
            normalized,
            "--json",
        ]
        if require_pass:
            args.append("--require-pass")
        return run_command(args)
    if phase == 4:
        args = [sys.executable, str(ROOT / "scripts" / "validate-quality-report.py"), "--story", str(story)]
        if require_pass:
            args.append("--require-pass")
        return run_command(args)
    phase_arg = phase_key(phase, normalized)
    return run_command([sys.executable, str(ROOT / "scripts" / "validate-story.py"), "--story", str(story), "--phase", phase_arg])


def run_phase(args: argparse.Namespace, story: Path, run_dir: Path, summary: Path, phase: int, retry: int) -> bool:
    phase_started = now_stamp()
    start = time.time()
    mode = normalize_pipeline_mode(args.mode)
    bundle = load_phase_bundle(phase, ROOT, mode)
    prompt_path = run_dir / f"phase{phase}.prompt.md"
    prompt_manifest = run_dir / f"phase{phase}.prompt-manifest.json"
    prompt_text, manifest = render_phase_prompt(story, phase, ROOT, mode)
    write_text(prompt_path, prompt_text)
    write_json(prompt_manifest, manifest)

    if args.dry_run:
        append_summary(summary, phase, "planned", phase_started, int(time.time() - start), retry, args.runner, "-", "dry-run prompt rendered")
        return True

    if phase == phase_for_role(mode, "final"):
        gate = validate_phase(story, phase_for_role(mode, "critic"), require_pass=True, mode=mode)
        (run_dir / f"phase{phase}.preflight-quality-gate.log").write_text(gate.stdout + gate.stderr, encoding="utf-8")
        if gate.returncode != 0:
            append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, "-", "quality gate failed before finalizer")
            return False

    runner_cmd = runner_args(args.runner, story, phase, prompt_path, run_dir, args.model, mode)
    result, runner_timing = run_command_with_heartbeat(
        runner_cmd,
        run_dir,
        phase,
        args.runner,
        float(args.heartbeat_seconds),
    )
    runner_log = run_dir / f"phase{phase}.runner.log"
    runner_log.write_text(result.stdout + result.stderr, encoding="utf-8")
    try:
        runner_result = json.loads(result.stdout.strip().splitlines()[-1]) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        runner_result = {}
    provider = str(runner_result.get("provider", ""))
    output_bundle = Path(runner_result.get("output_bundle", run_dir / f"phase{phase}.model.out"))
    phase_audit = {
        f"phase_{phase}_runner_timing": runner_timing,
        f"phase_{phase}_audit": {
            "phase": phase,
            "role": bundle.role,
            "runner": args.runner,
            "provider": provider,
            "selected_providers": runner_result.get("selected_providers", []),
            "model_or_command": runner_result.get("model_or_command", ""),
            "output_bundle": str(output_bundle),
            "attempts": runner_result.get("attempts", []),
            "runner_timing": runner_timing,
        }
    }

    if result.returncode != 0 or runner_result.get("status") != "success":
        notes = runner_result.get("failure_reason") or f"runner failed; see {runner_log.name}"
        append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, provider, str(notes))
        update_manifest(run_dir, {"last_failure": notes, "last_provider": provider, **phase_audit})
        return False

    live_story = story
    with StagedStory(story, run_dir, phase) as staged:
        story = staged.path
        update_manifest(run_dir, {f"phase_{phase}_attempt_tree": str(staged.path)})
        try:
            parse_report = apply_artifact_bundle(story, phase, output_bundle.read_text(encoding="utf-8"), run_dir, ROOT, mode, staged=True)
        except (OSError, ValueError) as exc:
            append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, provider, f"artifact parse failed: {exc}")
            write_json(run_dir / f"phase{phase}.parse-report.json", {"phase": phase, "status": "failed", "error": str(exc)})
            update_manifest(run_dir, phase_audit)
            return False

        if mode in {"production", "production_v6", "ultra_short"}:
            try:
                normalization = normalize_story(story, phase, mode, runner=args.runner, provider=provider)
            except Exception as exc:
                append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, provider, f"normalizer failed: {exc}")
                write_json(run_dir / f"phase{phase}.normalizer.log", {"phase": phase, "status": "failed", "error": str(exc)})
                update_manifest(run_dir, phase_audit)
                return False
            write_json(run_dir / f"phase{phase}.normalizer.log", normalization)

            try:
                from auto_repair import run_repair_pass
                repair_result = run_repair_pass(story, phase, mode)
                write_json(run_dir / f"phase{phase}.repair-report.json", repair_result)
                if phase == phase_for_role(mode, "final"):
                    normalize_story(story, phase, mode, runner=args.runner, provider=provider)
            except Exception as exc:
                write_json(run_dir / f"phase{phase}.repair-report.json", {"status": "fail", "error": str(exc)})

        validation = validate_phase(story, phase, require_pass=phase >= phase_for_role(mode, "critic"), mode=mode)
        (run_dir / f"phase{phase}.validator.log").write_text(validation.stdout + validation.stderr, encoding="utf-8")
        if validation.returncode != 0:
            append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, provider, "validator failed")
            update_manifest(run_dir, {"last_failure": "validator failed", "last_provider": provider, **phase_audit})
            return False

        # Tomato rubric gate runs on the current final-packager output. Failure marks
        # the phase as failed so the retry loop can do targeted rework.
        if mode in {"production", "production_v6", "ultra_short"} and phase == phase_for_role(mode, "final") and not args.dry_run and not args.skip_rubric and RUBRIC_CONFIG.get("enabled", True):
            threshold = float(getattr(args, "rubric_threshold", None) or RUBRIC_CONFIG.get("pass_threshold", 8.0))
            rubric_cmd = [
                sys.executable,
                str(ROOT / "scripts" / "tomato-rubric-score.py"),
                "--story", str(story),
                "--threshold", str(threshold),
                "--write-report",
                "--json",
            ]
            rubric_proc = run_command(rubric_cmd)
            (run_dir / f"phase{phase}.rubric.log").write_text(rubric_proc.stdout + rubric_proc.stderr, encoding="utf-8")
            if rubric_proc.returncode != 0:
                try:
                    rubric_payload = json.loads(rubric_proc.stdout) if rubric_proc.stdout.strip() else {}
                except json.JSONDecodeError:
                    rubric_payload = {}
                score = rubric_payload.get("overall_score", "?")
                notes = f"tomato rubric below threshold (score={score} thr={threshold})"
                append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, provider, notes)
                update_manifest(run_dir, {"last_failure": notes, "last_provider": provider, **phase_audit})
                return False
        report_path = story / "quality-report.json"
        if report_path.exists():
            report_data = load_json(report_path)
            metrics = report_data.get("machine_metrics", {})
            if isinstance(metrics, dict) and isinstance(metrics.get("text_path"), str):
                metrics["text_path"] = metrics["text_path"].replace(str(story), str(live_story.resolve()), 1)
                write_json(report_path, report_data)
        update_manifest(run_dir, {f"phase_{phase}_attempt_backup": str(staged.path)})
        try:
            staged.publish()
        except OSError as exc:
            append_summary(summary, phase, "failed", phase_started, int(time.time() - start), retry, args.runner, provider, f"publication failed: {exc}")
            return False
    story = live_story

    notes = f"{len(parse_report['written'])} artifacts ok"
    append_summary(summary, phase, "completed", phase_started, int(time.time() - start), retry, args.runner, provider, notes)
    update_manifest(
        run_dir,
        {
            "last_completed_phase": phase,
            "last_provider": provider,
            "last_runner": args.runner,
            "source_access": story_source_access(story),
            **phase_audit,
        },
    )
    update_story_automation(
        story,
        {
            "last_run_id": args.run_id,
            "runner": args.runner,
            "provider": provider,
            "current_phase": phase,
            "retry_count": retry,
            "phase2_blueprint_review": "skipped" if args.no_human_gates or args.runner == "mock" else "pending",
        },
    )
    if phase == 2 and not args.no_human_gates and args.runner != "mock" and bundle.human_gate != "none":
        append_summary(summary, phase, "paused", phase_started, int(time.time() - start), retry, args.runner, provider, f"waiting for human gate: {bundle.human_gate}")
        return False
    return True


def run_pipeline(args: argparse.Namespace) -> int:
    try:
        with story_write_lock(Path(args.story)):
            return _run_pipeline(args)
    except (OSError, ValueError, ImportError) as exc:
        eprint(f"Unable to run safely: {exc}")
        return RUNNER_EXIT_VALIDATION_FAILED


def _run_pipeline(args: argparse.Namespace) -> int:
    args.mode = normalize_pipeline_mode(args.mode)
    story = Path(args.story)
    if not story.exists():
        eprint(f"story directory does not exist: {story}")
        return 11
    if not args.dry_run and not (story / "source.md").exists():
        eprint(f"missing source.md: {story / 'source.md'}")
        return 11
    if story_source_access(story) == "denied" and args.runner in {"agent", "codex", "openclaw", "claude"}:
        eprint(f"source_policy.access=denied blocks runner {args.runner}")
        return 30

    try:
        validate_bundle_schema(ROOT, args.mode)
    except ValueError as exc:
        eprint(str(exc))
        return 11

    if not args.run_id:
        args.run_id = now_run_id()
    run_dir = story / "runs" / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    summary = init_summary(story, run_dir, args.run_id, args.runner, args.from_phase, args.max_retries)
    update_manifest(
        run_dir,
        {
            "run_id": args.run_id,
            "story": str(story),
            "runner": args.runner,
            "mode": args.mode,
            "from_phase": args.from_phase,
            "max_retries": args.max_retries,
            "source_access": story_source_access(story),
            "started_at": now_stamp(),
        },
    )

    if args.dry_run:
        print(f"[DRY-RUN] StoryForge run initialized: {run_dir}")

    phase = args.from_phase
    retry = 0
    max_phase = min(phase_count(args.mode), args.to_phase or phase_count(args.mode))
    if args.to_phase and args.to_phase < args.from_phase:
        eprint(f"--to-phase ({args.to_phase}) must be >= --from-phase ({args.from_phase})")
        return 11
    review_phase = phase_for_role(args.mode, "critic")
    rewrite_phase = phase_for_role(args.mode, "scene")
    while phase <= max_phase:
        try:
            ok = run_phase(args, story, run_dir, summary, phase, retry)
        except (OSError, ValueError) as exc:
            eprint(f"phase {phase} failed safely: {exc}")
            return RUNNER_EXIT_VALIDATION_FAILED
        if ok:
            phase += 1
            continue

        if phase == review_phase and retry < args.max_retries:
            retry += 1
            draft = story / "draft.md"
            if draft.exists() and not args.dry_run:
                shutil.copy2(draft, story / f"draft-v{retry}.md")
            if args.mode in {"production", "production_v6", "ultra_short"} and not args.dry_run:
                scenes_dir = story / "draft-scenes"
                backup_dir = story / f"draft-scenes-v{retry}"
                if scenes_dir.exists() and not backup_dir.exists():
                    shutil.copytree(scenes_dir, backup_dir)
            update_story_automation(
                story,
                {
                    "last_run_id": args.run_id,
                    "runner": args.runner,
                    "provider": "",
                    "current_phase": rewrite_phase,
                    "retry_count": retry,
                    "phase2_blueprint_review": "skipped" if args.no_human_gates or args.runner == "mock" else "approved",
                },
            )
            phase = rewrite_phase
            continue
        if args.mode in {"production", "production_v6", "ultra_short"} and phase == rewrite_phase and retry < args.max_retries:
            retry += 1
            draft = story / "draft.md"
            if draft.exists() and not args.dry_run:
                shutil.copy2(draft, story / f"draft-v{retry}.md")
            if not args.dry_run:
                scenes_dir = story / "draft-scenes"
                backup_dir = story / f"draft-scenes-v{retry}"
                if scenes_dir.exists() and not backup_dir.exists():
                    shutil.copytree(scenes_dir, backup_dir)
            update_story_automation(
                story,
                {
                    "last_run_id": args.run_id,
                    "runner": args.runner,
                    "provider": "",
                    "current_phase": rewrite_phase,
                    "retry_count": retry,
                    "phase2_blueprint_review": "skipped" if args.no_human_gates or args.runner == "mock" else "approved",
                },
            )
            phase = rewrite_phase
            continue
        if args.mode in {"production", "production_v6", "ultra_short"} and phase == phase_for_role(args.mode, "final") and retry < args.max_retries:
            retry += 1
            if not args.dry_run:
                final = story / "final.md"
                if final.exists():
                    shutil.copy2(final, story / f"final-v{retry}.md")
            update_story_automation(
                story,
                {
                    "last_run_id": args.run_id,
                    "runner": args.runner,
                    "provider": "",
                    "current_phase": rewrite_phase,
                    "retry_count": retry,
                    "phase2_blueprint_review": "skipped" if args.no_human_gates or args.runner == "mock" else "approved",
                },
            )
            phase = phase_for_role(args.mode, "final")
            continue
        if phase == 2 and not args.no_human_gates and args.runner != "mock":
            print(f"Human gate required. Approve with: python3 scripts/storyforge.py approve-gate --story {story} --gate phase2_blueprint_review")
            return RUNNER_EXIT_HUMAN_GATE
        return RUNNER_EXIT_VALIDATION_FAILED

    with summary.open("a", encoding="utf-8") as handle:
        handle.write(f"\n**Ended**: {now_stamp()}\n")
    update_manifest(run_dir, {"status": "completed", "ended_at": now_stamp(), "ended_phase": max_phase})
    print(f"StoryForge run completed: {run_dir}")
    return 0


def approve_gate(args: argparse.Namespace) -> int:
    story = Path(args.story)
    if args.gate != "phase2_blueprint_review":
        eprint(f"unknown gate: {args.gate}")
        return 10
    update_story_automation(
        story,
        {
            "phase2_blueprint_review": "approved",
        },
    )
    print(f"gate approved: {args.gate}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="storyforge.py")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run")
    run.add_argument("--story", required=True)
    run.add_argument("--from-phase", "--phase", type=int, choices=range(1, 10), default=1)
    run.add_argument("--runner", default="agent", choices=["agent", "codex", "openclaw", "claude", "mock", "manual-prompt-pack", "local-ollama"])
    run.add_argument("--mode", default="v4", choices=["v4", "full", "fast", "production", "prod", "production_v6", "prod_v6", "v6", "ultra_short", "ultrashort", "short"])
    run.add_argument("--run-id", default="")
    run.add_argument("--to-phase", type=int, choices=range(1, 10), default=None)
    run.add_argument("--max-retries", type=int, default=3)
    run.add_argument("--model", default="")
    run.add_argument("--heartbeat-seconds", type=float, default=float(os.environ.get("STORYFORGE_HEARTBEAT_SECONDS", "30")))
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--no-human-gates", action="store_true")
    run.add_argument("--skip-rubric", action="store_true", help="skip tomato rubric gate after the final-packager phase")
    run.add_argument("--rubric-threshold", type=float, default=float(os.environ.get("STORYFORGE_RUBRIC_THRESHOLD", "0")) or None)
    run.set_defaults(func=run_pipeline)

    gate = sub.add_parser("approve-gate")
    gate.add_argument("--story", required=True)
    gate.add_argument("--gate", required=True)
    gate.add_argument("--run-id", default="")
    gate.set_defaults(func=approve_gate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
