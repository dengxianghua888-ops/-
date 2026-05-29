#!/usr/bin/env python3
"""Extract per-chapter quantitative metrics from source text.

Splits source by chapter markers (## 第X章, ## Chapter X, etc.) and computes
rhythm metrics for each chapter. Outputs the machine-calculable Section A of
chapter-soul-map.json. LLM fills the remaining 6 dimensions (B-G).

Usage:
    python chapter_soul_extractor.py --source story/source.md --output story/analysis/chapter-soul-map-metrics.json
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))

from rhythm_metrics import (
    compute_comma_period_ratio,
    compute_sentence_avg_len,
    count_nonspace,
    rhythm_profile,
    QUOTE_RE,
)

CHAPTER_SPLIT_RE = re.compile(
    r"^(?:#{1,3}\s*)?(?:第[一二三四五六七八九十百千\d]+章|Chapter\s*\d+|[一二三四五六七八九十]+、)",
    re.MULTILINE,
)


def split_chapters(text: str) -> List[Tuple[int, int, str]]:
    """Split source text into chapters. Returns list of (start_line, end_line, text)."""
    lines = text.splitlines()
    chapter_starts: List[int] = []

    for i, line in enumerate(lines):
        if CHAPTER_SPLIT_RE.match(line.strip()):
            chapter_starts.append(i)

    if not chapter_starts:
        return [(1, len(lines), text)]

    chapters: List[Tuple[int, int, str]] = []
    for idx, start in enumerate(chapter_starts):
        end = chapter_starts[idx + 1] if idx + 1 < len(chapter_starts) else len(lines)
        chapter_text = "\n".join(lines[start:end])
        chapters.append((start + 1, end, chapter_text))

    return chapters


def chapter_metrics(text: str) -> Dict[str, Any]:
    """Compute Section A metrics for a single chapter."""
    profile = rhythm_profile(text)
    comma_ratio = compute_comma_period_ratio(text)
    sentence_avg = compute_sentence_avg_len(text)

    lines_content = [
        ln.strip() for ln in text.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    total_lines = len(lines_content) if lines_content else 1
    dialogue_lines = sum(1 for ln in lines_content if QUOTE_RE.search(ln))
    question_marks = text.count("？") + text.count("?")
    chars = count_nonspace(text)

    return {
        "avg_line_chars": profile["avg_line_chars"],
        "comma_period_ratio": comma_ratio,
        "question_mark_density_per_1k": round(question_marks / max(chars / 1000, 1e-6), 2),
        "direct_dialogue_rate": round(dialogue_lines / total_lines, 3),
        "short_line_rate_lte16": profile["short_line_rate"],
        "impact_density": round(profile.get("question_marks_per_k", 0) / 10, 2),
        "sentence_avg_len": sentence_avg,
    }


def suggest_slices(char_count: int) -> int:
    """Suggest number of scene slices for a chapter based on char count."""
    if char_count <= 1000:
        return 1
    if char_count <= 2000:
        return 2
    return math.ceil(char_count / 800)


def extract(source_path: Path) -> Dict[str, Any]:
    """Full extraction: split chapters and compute metrics."""
    text = source_path.read_text(encoding="utf-8")
    chapters = split_chapters(text)

    result_chapters = []
    for idx, (start_line, end_line, ch_text) in enumerate(chapters, 1):
        chars = count_nonspace(ch_text)
        metrics = chapter_metrics(ch_text)
        slices = suggest_slices(chars)

        result_chapters.append({
            "chapter_id": idx,
            "source_line_range": [start_line, end_line],
            "char_count": chars,
            "suggested_slices": slices,
            "metrics": metrics,
            "emotion": {},
            "highlights": {},
            "techniques": [],
            "golden_lines": [],
            "narrative_mode": "",
            "rhythm_shape": "",
            "pacing_note": "",
            "chapter_end_hook": {},
        })

    return {
        "source_file": str(source_path.name),
        "total_chapters": len(result_chapters),
        "total_chars": count_nonspace(text),
        "chapters": result_chapters,
        "global_soul_signature": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract per-chapter rhythm metrics from source text")
    parser.add_argument("--source", required=True, help="Path to source.md")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: source file not found: {source_path}")
        return 1

    result = extract(source_path)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Extracted {result['total_chapters']} chapters → {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
