#!/usr/bin/env python3
"""Validate StoryForge V4 story artifact completeness and quality gate."""

import argparse
import sys
from pathlib import Path

from v4_quality import (
    VALID_STORY_STATUSES,
    count_nonspace,
    count_hits,
    eprint,
    load_workspace_policy,
    load_story_manifest,
    missing_artifacts,
    normalize_phase,
    validate_quality_report,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True, help="Path to stories/{slug}")
    parser.add_argument(
        "--phase",
        default="final",
        help="Required phase/artifact level: phase1, phase2, draft, review, final",
    )
    args = parser.parse_args()

    story = Path(args.story)
    try:
        phase = normalize_phase(args.phase)
    except ValueError as exc:
        eprint(str(exc))
        return 1

    if not story.is_dir():
        eprint(f"story directory does not exist: {story}")
        return 1

    missing = missing_artifacts(story, phase)
    if missing:
        eprint("missing required artifacts:")
        for rel in missing:
            eprint(f"- {rel}")
        return 1

    review_gate = None
    if phase in {"review", "final"}:
        try:
            review_gate, _report = validate_quality_report(story)
        except ValueError as exc:
            eprint(str(exc))
            return 1
        if phase == "final" and review_gate["gate_status"] != "pass":
            eprint("final phase requires gate_status=pass")
            return 1

    if phase == "final":
        try:
            manifest = load_story_manifest(story)
        except ValueError as exc:
            eprint(str(exc))
            return 1
        status = manifest.get("status")
        if status not in VALID_STORY_STATUSES:
            eprint(f"story.yaml status must be one of {sorted(VALID_STORY_STATUSES)}")
            return 1
        if status not in {"final", "submitted"}:
            eprint("story.yaml status must be final or submitted for final validation")
            return 1
        slug = manifest.get("slug")
        if slug and slug != story.name:
            eprint(f"story.yaml slug {slug!r} does not match directory {story.name!r}")
            return 1
        if review_gate:
            manifest_gate = manifest.get("quality_gate", {})
            if isinstance(manifest_gate, dict):
                gate_status = manifest_gate.get("gate_status")
                if gate_status and gate_status != review_gate["gate_status"]:
                    eprint("story.yaml quality_gate.gate_status does not match review.md")
                    return 1
        output_title = manifest.get("output_title")
        target_platform = str(manifest.get("target_platform", ""))
        policy = load_workspace_policy(story)
        title_max_chars = int(policy.get("title_max_chars", 30))
        if output_title and target_platform == "tomato" and count_nonspace(str(output_title)) > title_max_chars:
            eprint(f"story.yaml output_title exceeds {title_max_chars} chars for tomato")
            return 1

        final_text = (story / "final.md").read_text(encoding="utf-8")
        genre = str(manifest.get("genre", ""))
        hard_terms = list(policy.get("forbidden_words", []))
        hard_terms.extend(policy.get("genre_extra_forbidden", {}).get(genre, []))
        hard_hits = count_hits(final_text, hard_terms)
        if hard_hits:
            eprint(f"hard forbidden words remain in final.md: {hard_hits}")
            return 1
        soft_hits = count_hits(final_text, policy.get("soft_forbidden", []))
        soft_total = sum(soft_hits.values())
        if soft_total > int(policy.get("soft_forbidden_max", 2)):
            eprint(f"soft forbidden words exceed limit in final.md: {soft_hits}")
            return 1

    print(f"story ok: {story} phase={phase}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
