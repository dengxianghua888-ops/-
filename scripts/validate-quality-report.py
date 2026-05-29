#!/usr/bin/env python3
"""Validate StoryForge V4 review.md + quality-report.json gate output."""

import argparse
import sys
from pathlib import Path

from v4_quality import eprint, validate_quality_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True, help="Path to stories/{slug}")
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Return non-zero unless the structured quality gate is pass",
    )
    args = parser.parse_args()

    story = Path(args.story)
    try:
        review_gate, _report = validate_quality_report(story)
    except ValueError as exc:
        eprint(str(exc))
        return 1

    if args.require_pass and review_gate["gate_status"] != "pass":
        eprint("quality gate failed: gate_status=fail")
        return 1

    print(
        f"quality report ok: story={story} "
        f"gate_status={review_gate['gate_status']} "
        f"critical_failures={len(review_gate['critical_failures'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
