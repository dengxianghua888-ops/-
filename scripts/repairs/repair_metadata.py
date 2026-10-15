"""F4 repairer: keep story.yaml + tomato-submission table head + chapters-map
in sync with quality-report.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _patch_yaml_field(text: str, key: str, value: Any) -> str:
    pattern = re.compile(rf"^({re.escape(key)}\s*:\s*).*$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(rf"\g<1>{value}", text, count=1)
    return text.rstrip() + f"\n{key}: {value}\n"


def _patch_yaml_block(text: str, parent: str, child: str, value: Any) -> str:
    """Patch ``parent.child`` in a 2-level YAML block. Adds the parent if missing."""
    parent_pattern = re.compile(rf"^{re.escape(parent)}:\s*$", re.MULTILINE)
    if not parent_pattern.search(text):
        text = text.rstrip() + f"\n{parent}:\n  {child}: {value}\n"
        return text
    child_pattern = re.compile(
        rf"(^{re.escape(parent)}:\s*\n(?:[ \t]+.*\n)*?[ \t]+){re.escape(child)}\s*:\s*.*$",
        re.MULTILINE,
    )
    if child_pattern.search(text):
        return child_pattern.sub(rf"\g<1>{child}: {value}", text, count=1)
    insertion_pattern = re.compile(rf"^{re.escape(parent)}:\s*\n", re.MULTILINE)
    return insertion_pattern.sub(f"{parent}:\n  {child}: {value}\n", text, count=1)


def run(story: Path, mode: str = "production") -> Dict[str, Any]:
    report_path = story / "quality-report.json"
    if not report_path.exists():
        return {"name": "metadata", "status": "skipped", "reason": "no quality-report.json"}
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"name": "metadata", "status": "fail", "reason": "invalid JSON"}

    metrics = report.get("machine_metrics", {}) or {}
    target = metrics.get("target_length", {}) or {}
    chapters = metrics.get("chapters", {}) or {}
    paywall = metrics.get("paywall_cards", {}) or {}
    critic = report.get("critic_scores", {}) or {}
    gate_status = str(report.get("gate_status", "")).lower()

    patched: Dict[str, Any] = {}
    yaml_path = story / "story.yaml"
    if yaml_path.exists():
        text = yaml_path.read_text(encoding="utf-8")
        original = text
        if gate_status == "pass" and not re.search(r"^status:\s*test_fixture\s*$", text, re.MULTILINE):
            text = _patch_yaml_field(text, "status", "final")
        if target.get("actual"):
            text = _patch_yaml_field(text, "total_chars", int(target["actual"]))
        if chapters.get("count"):
            text = _patch_yaml_field(text, "chapter_count", int(chapters["count"]))
        if paywall.get("actual"):
            text = _patch_yaml_field(text, "paywall_cards", int(paywall["actual"]))
        if gate_status:
            text = _patch_yaml_field(text, "quality_gate", gate_status)
        for k in ("platform", "emotion", "style", "logic"):
            if k in critic:
                text = _patch_yaml_block(text, "critic_scores", k, critic[k])
        if text != original:
            yaml_path.write_text(text, encoding="utf-8")
            patched["story.yaml"] = True

    submission_path = story / "tomato-submission.md"
    if submission_path.exists() and chapters.get("count"):
        body = submission_path.read_text(encoding="utf-8")
        new_body = re.sub(
            r"^- 章节数:\s*\d+",
            f"- 章节数: {int(chapters['count'])}",
            body,
            count=1,
            flags=re.MULTILINE,
        )
        new_body = re.sub(
            r"^- 总字数:\s*\d+",
            f"- 总字数: {int(target.get('actual', 0))}",
            new_body,
            count=1,
            flags=re.MULTILINE,
        )
        if new_body != body:
            submission_path.write_text(new_body, encoding="utf-8")
            patched["tomato-submission.md"] = True

    return {"name": "metadata", "status": "ok", "patched": patched}


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--mode", default="production")
    args = parser.parse_args()
    result = run(Path(args.story), args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)
