#!/usr/bin/env python3
"""Report StoryForge corpus readiness for V4 few-shot retrieval."""

import argparse
import collections
import json
import sys
from pathlib import Path

from v4_quality import eprint

GENE_FIELDS = (
    "reader_promise",
    "emotional_debt_type",
    "dominant_s爽点",
    "antagonist_violation",
    "protagonist_stance",
    "payoff_pattern",
    "tomato_fit_score",
)


def has_v4_genes(entry):
    return all(key in entry for key in GENE_FIELDS)


def build_report(index_path: Path):
    idx = json.loads(index_path.read_text(encoding="utf-8"))
    entries = idx.get("entries", [])
    total = len(entries)
    dissected = [entry for entry in entries if entry.get("status") == "dissected"]
    pending = [entry for entry in entries if entry.get("status") != "dissected"]
    genre_counts = collections.Counter(entry.get("genre", "(missing)") for entry in dissected)
    mechanism_counts = collections.Counter(
        mech for entry in dissected for mech in entry.get("reversal_mechanisms", [])
    )
    gene_complete = [entry for entry in dissected if has_v4_genes(entry)]
    human_calibrated = [
        entry for entry in gene_complete if entry.get("v4_calibration_status") == "human_calibrated"
    ]
    machine_draft = [
        entry for entry in gene_complete if entry.get("v4_calibration_status") == "machine_draft"
    ]
    goal_per_genre = 2
    human_by_genre = {}
    for genre in sorted(set(entry.get("genre", "(missing)") for entry in dissected)):
        available = [entry for entry in gene_complete if entry.get("genre", "(missing)") == genre]
        calibrated = [entry for entry in human_calibrated if entry.get("genre", "(missing)") == genre]
        candidates = [entry for entry in machine_draft if entry.get("genre", "(missing)") == genre]
        available_target = min(goal_per_genre, len(available))
        human_by_genre[genre] = {
            "available": len(available),
            "available_target": available_target,
            "calibrated": len(calibrated),
            "deficit": max(0, available_target - len(calibrated)),
            "full_goal_deficit": max(0, goal_per_genre - len(calibrated)),
            "candidate_slugs": [entry["slug"] for entry in sorted(
                candidates,
                key=lambda item: (-float(item.get("tomato_fit_score", 0) or 0), item.get("slug", "")),
            )[:goal_per_genre]],
        }
    return {
        "total": total,
        "dissected": len(dissected),
        "pending": len(pending),
        "completion_rate": round(len(dissected) / total, 4) if total else 0,
        "genre_counts": dict(sorted(genre_counts.items())),
        "mechanism_counts": dict(sorted(mechanism_counts.items())),
        "gene_complete": len(gene_complete),
        "gene_completion_rate": round(len(gene_complete) / len(dissected), 4) if dissected else 0,
        "machine_draft_genes": [entry["slug"] for entry in machine_draft],
        "human_calibrated_genes": [entry["slug"] for entry in human_calibrated],
        "human_calibration": {
            "goal_per_genre": goal_per_genre,
            "by_genre": human_by_genre,
            "available_target_total": sum(item["available_target"] for item in human_by_genre.values()),
            "calibrated_total": len(human_calibrated),
            "deficit_total": sum(item["deficit"] for item in human_by_genre.values()),
        },
        "missing_genes": [
            entry["slug"]
            for entry in dissected
            if not has_v4_genes(entry)
        ],
        "pending_slugs": [entry["slug"] for entry in pending],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index",
        default=str(Path(__file__).resolve().parent.parent / "corpus" / "_index.json"),
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.index)
    if not path.exists():
        eprint(f"missing corpus index: {path}")
        return 1
    try:
        report = build_report(path)
    except json.JSONDecodeError as exc:
        eprint(f"invalid JSON in {path}: {exc}")
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Corpus: {report['dissected']}/{report['total']} dissected ({report['completion_rate']:.0%})")
        print(
            f"V4 genes: {report['gene_complete']}/{report['dissected']} complete "
            f"({report['gene_completion_rate']:.0%})"
        )
        print(f"Genres: {report['genre_counts']}")
        print(f"Mechanisms: {report['mechanism_counts']}")
        print(f"Pending: {len(report['pending_slugs'])}")
        print(f"Missing V4 genes: {len(report['missing_genes'])}")
        print(f"Machine draft genes: {len(report['machine_draft_genes'])}")
        print(f"Human calibrated genes: {len(report['human_calibrated_genes'])}")
        hc = report["human_calibration"]
        print(
            f"Human calibration target: {hc['calibrated_total']}/"
            f"{hc['available_target_total']} complete, deficit {hc['deficit_total']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
