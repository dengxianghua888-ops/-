#!/usr/bin/env python3
"""Render a StoryForge phase prompt from a phase bundle."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from storyforge_lib import render_phase_prompt, repo_root, write_json, write_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--phase", required=True, type=int, choices=range(1, 9))
    parser.add_argument("--mode", default="v4")
    parser.add_argument("--out")
    parser.add_argument("--manifest")
    args = parser.parse_args()

    story = Path(args.story)
    if not story.is_dir():
        print(f"story directory does not exist: {story}", file=sys.stderr)
        return 1

    try:
        prompt, manifest = render_phase_prompt(story, args.phase, repo_root(), args.mode)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.out:
        write_text(Path(args.out), prompt)
    else:
        print(prompt, end="")
    if args.manifest:
        write_json(Path(args.manifest), manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
