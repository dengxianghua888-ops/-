#!/usr/bin/env python3
"""Compute machine-checkable StoryForge style and AI-flavor metrics."""

import argparse
import json
import sys
from pathlib import Path

from v4_quality import count_hits, eprint, load_story_manifest, load_workspace_policy, style_metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True, help="Path to stories/{slug}")
    parser.add_argument("--file", default=None, help="Specific markdown file to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args()

    story = Path(args.story)
    target = Path(args.file) if args.file else story / "final.md"
    if not target.exists() and not args.file:
        target = story / "draft.md"
    if not target.exists():
        eprint(f"missing text file: {target}")
        return 1

    text = target.read_text(encoding="utf-8")
    metrics = style_metrics(text)
    policy = load_workspace_policy(story)
    genre = ""
    manifest = story / "story.yaml"
    if manifest.exists():
        try:
            genre = str(load_story_manifest(story).get("genre", ""))
        except ValueError:
            genre = ""
    hard_terms = list(policy.get("forbidden_words", []))
    hard_terms.extend(policy.get("genre_extra_forbidden", {}).get(genre, []))
    metrics["forbidden_hits"] = count_hits(text, hard_terms)
    metrics["soft_forbidden_hits"] = count_hits(text, policy.get("soft_forbidden", []))
    if args.json:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    else:
        print(f"file: {target}")
        for key, value in metrics.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
