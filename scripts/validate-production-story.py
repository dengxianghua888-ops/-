#!/usr/bin/env python3
"""Validate StoryForge production-mode artifacts and hard quality metrics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from production_quality import validate_story


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--phase", required=True, type=int, choices=range(1, 10))
    parser.add_argument("--mode", default="production", choices=["production", "production_v6", "ultra_short"])
    parser.add_argument("--require-pass", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    story = Path(args.story)
    if not story.is_dir():
        print(f"story directory does not exist: {story}", file=sys.stderr)
        return 1

    try:
        result = validate_story(story, args.phase, args.mode, require_pass=args.require_pass)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["status"] == "pass":
        print(f"production story ok: story={story} phase={args.phase} mode={args.mode}")
    else:
        print("production quality failed:", file=sys.stderr)
        for failure in result["failures"]:
            print(f"- {failure}", file=sys.stderr)

    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
