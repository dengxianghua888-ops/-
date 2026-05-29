"""F5 pre-warning: scan draft scenes for forbidden / soft-forbidden hits before
critic phase. Writes ``scene-forbidden-scan.json`` listing per-scene matches.
This never edits content - it only surfaces hits earlier in the pipeline.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]


def _load_forbidden() -> Dict[str, List[str]]:
    forbidden: List[str] = []
    soft: List[str] = []

    learned = ROOT / "context" / "forbidden-words-learned.json"
    if learned.exists():
        try:
            data = json.loads(learned.read_text(encoding="utf-8"))
            forbidden.extend(data.get("forbidden_words", []) or [])
            soft.extend(data.get("soft_forbidden", []) or [])
        except json.JSONDecodeError:
            pass

    workspace = ROOT / "workspace.yaml"
    if workspace.exists():
        text = workspace.read_text(encoding="utf-8")
        forbidden.extend(_parse_yaml_list(text, "forbidden_words"))
        soft.extend(_parse_yaml_list(text, "soft_forbidden"))

    return {
        "forbidden": sorted(set(w for w in forbidden if w)),
        "soft": sorted(set(w for w in soft if w)),
    }


def _parse_yaml_list(text: str, key: str) -> List[str]:
    pattern = re.compile(
        rf"^\s*{re.escape(key)}\s*:\s*\n((?:\s+-\s+.*\n)+)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return []
    items: List[str] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        value = stripped[1:].strip().strip('"').strip("'")
        if value:
            items.append(value)
    return items


def run(story: Path, mode: str = "production") -> Dict[str, Any]:
    scenes_dir = story / "draft-scenes"
    if not scenes_dir.is_dir():
        return {"name": "forbidden_scan", "status": "skipped", "reason": "no draft-scenes"}

    catalog = _load_forbidden()
    scan_results: List[Dict[str, Any]] = []
    total_hard = 0
    total_soft = 0
    for scene in sorted(scenes_dir.glob("*.md")):
        text = scene.read_text(encoding="utf-8")
        hard_hits = {w: text.count(w) for w in catalog["forbidden"] if w in text}
        soft_hits = {w: text.count(w) for w in catalog["soft"] if w in text}
        if hard_hits or soft_hits:
            scan_results.append({
                "scene": scene.name,
                "forbidden": hard_hits,
                "soft_forbidden": soft_hits,
            })
        total_hard += sum(hard_hits.values())
        total_soft += sum(soft_hits.values())

    out_path = story / "scene-forbidden-scan.json"
    out_path.write_text(
        json.dumps(
            {
                "totals": {"forbidden": total_hard, "soft_forbidden": total_soft},
                "per_scene": scan_results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    status = "ok"
    if total_hard:
        status = "manual_review_required"
    return {
        "name": "forbidden_scan",
        "status": status,
        "totals": {"forbidden": total_hard, "soft_forbidden": total_soft},
        "report_path": str(out_path.relative_to(story)),
    }


if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--mode", default="production")
    args = parser.parse_args()
    result = run(Path(args.story), args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)
