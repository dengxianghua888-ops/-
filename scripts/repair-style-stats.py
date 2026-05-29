#!/usr/bin/env python3
"""Repair StoryForge style stats, especially percent-vs-ratio drift."""

import argparse
import json
import sys
from pathlib import Path

from v4_quality import eprint, normalize_ratio_value, stats


def repair(doc):
    changed = 0
    for _genre, fields in doc.get("by_genre", {}).items():
        ratio = fields.get("dialogue_ratio")
        if not isinstance(ratio, dict):
            continue
        samples = ratio.get("samples", [])
        normalized = [normalize_ratio_value(value) for value in samples]
        if normalized != samples:
            changed += 1
        ratio.update(stats(normalized))
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stats",
        default=str(Path(__file__).resolve().parent.parent / "context" / "style-dna-stats.json"),
    )
    args = parser.parse_args()

    path = Path(args.stats)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        eprint(f"missing stats file: {path}")
        return 1
    except json.JSONDecodeError as exc:
        eprint(f"invalid JSON in {path}: {exc}")
        return 1

    changed = repair(doc)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"repaired style stats: {path} normalized_fields={changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
