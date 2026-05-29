"""F2 repairer: rebuild quality-report.json machine_metrics from production_quality.

Replaces the stale ``machine_metrics`` section with a freshly computed snapshot
based on current artifact state. Critic scores and gate evidence are left
untouched.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from production_quality import machine_evaluate  # noqa: E402


def run(story: Path, mode: str = "production") -> Dict[str, Any]:
    report_path = story / "quality-report.json"
    if not report_path.exists():
        return {"name": "quality_report_sync", "status": "skipped", "reason": "no quality-report.json"}
    # Use phase=7 if final.md exists so machine_evaluate reads the canonical
    # post-packager output instead of the still-stale draft.md.
    use_phase = 7 if (story / "final.md").exists() else 6
    metrics = machine_evaluate(story, use_phase, mode)
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"name": "quality_report_sync", "status": "fail", "reason": "invalid JSON"}

    before = report.get("machine_metrics", {})
    report["machine_metrics"] = metrics
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    diffs = []
    for key in ("target_length", "chapters", "paywall_cards", "style_metrics"):
        if before.get(key) != metrics.get(key):
            diffs.append(key)
    return {
        "name": "quality_report_sync",
        "status": "ok",
        "synced_sections": diffs,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--mode", default="production")
    args = parser.parse_args()
    result = run(Path(args.story), args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] in {"ok", "skipped"} else 1)
