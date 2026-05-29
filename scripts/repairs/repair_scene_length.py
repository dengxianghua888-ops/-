"""F3 repairer: detect scenes whose char count drifts outside target_chars range.

The repairer does not auto-rewrite scenes (that is a model job). Instead, it
emits a ``scene-rewrite-todo.json`` listing every offending scene with the
required delta. Phase 5 reruns can pick this up to do targeted rewrites.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


def _count_chars(text: str) -> int:
    body = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    return len(re.sub(r"\s", "", body))


def run(story: Path, mode: str = "production") -> Dict[str, Any]:
    cards_dir = story / "scene-cards"
    scenes_dir = story / "draft-scenes"
    if not cards_dir.is_dir() or not scenes_dir.is_dir():
        return {"name": "scene_length", "status": "skipped", "reason": "scene-cards or draft-scenes missing"}

    todos: List[Dict[str, Any]] = []
    summary: List[Dict[str, Any]] = []
    for card_path in sorted(cards_dir.glob("scene-*.json")):
        try:
            card = json.loads(card_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        scene_id = str(card.get("scene_id", card_path.stem))
        scene_file = scenes_dir / f"{scene_id}.md"
        if not scene_file.exists():
            todos.append({
                "scene_id": scene_id,
                "issue": "missing draft scene file",
                "delta": None,
            })
            continue
        actual = _count_chars(scene_file.read_text(encoding="utf-8"))
        lo = int(card.get("target_chars_min", 0) or 0)
        hi = int(card.get("target_chars_max", 0) or 0)
        entry = {"scene_id": scene_id, "actual_chars": actual, "min": lo, "max": hi}
        if lo and actual < lo:
            entry["delta"] = lo - actual
            entry["direction"] = "expand"
            todos.append(entry)
        elif hi and actual > hi:
            entry["delta"] = actual - hi
            entry["direction"] = "trim"
            todos.append(entry)
        summary.append(entry)

    todo_path = story / "scene-rewrite-todo.json"
    todo_path.write_text(
        json.dumps({"todos": todos, "summary": summary}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "name": "scene_length",
        "status": "ok" if not todos else "manual_review_required",
        "offending_scenes": [t["scene_id"] for t in todos],
        "todo_path": str(todo_path.relative_to(story)),
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
