#!/usr/bin/env python3
"""Sync story.yaml quality summary from quality-report.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def sync_story(story: Path) -> dict[str, object]:
    yaml_path = story / "story.yaml"
    report_path = story / "quality-report.json"
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) if yaml_path.exists() else {}
    report = json.loads(report_path.read_text(encoding="utf-8"))

    data.setdefault("quality_gate", {})
    data["quality_gate"].update(
        {
            "source_report": "story/quality-report.json",
            "schema_version": report.get("schema_version"),
            "pipeline_mode": report.get("pipeline_mode"),
            "gate_status": report.get("gate_status"),
            "critical_failures": report.get("critical_failures", []),
            "important_failures": report.get("important_failures", []),
            "machine_metrics": report.get("machine_metrics", {}),
            "critic_scores": report.get("critic_scores", {}),
        }
    )

    chapters = sorted((story / "final-chapters").glob("ch*.md"))
    data.setdefault("final_packaging", {})
    data["final_packaging"].update(
        {
            "final_file": "final.md",
            "craft_notes_file": "craft-notes.md",
            "submission_file": "tomato-submission.md",
            "chapters_map": "final-chapters/_chapters-map.md",
            "chapter_count": len(chapters),
            "chapter_files": [f"final-chapters/{path.name}" for path in chapters],
        }
    )
    revisions = data["final_packaging"].setdefault("revisions_applied", [])
    note = "直接投稿版优化：补导语、自然付费卡点、一句一段移动端格式。"
    if isinstance(revisions, list) and note not in revisions:
        revisions.append(note)

    yaml_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {
        "story": str(story),
        "chars": report.get("machine_metrics", {}).get("target_length", {}).get("actual"),
        "chapters": len(chapters),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stories", nargs="+")
    args = parser.parse_args()
    for raw in args.stories:
        print(json.dumps(sync_story(Path(raw)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
