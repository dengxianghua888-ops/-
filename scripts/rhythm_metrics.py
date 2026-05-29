#!/usr/bin/env python3
"""Compare source and generated story rhythm.

The production pipeline already checks length, hooks and safety. This module
adds a separate fidelity check for the things that make short fiction feel
fast on mobile: short visual lines, direct dialogue, and question pressure.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path
from typing import Any, Dict, List


SENTENCE_END_RE = re.compile(r"[。！？!?；;]")
COMMA_RE = re.compile(r"[，,、]")
PERIOD_RE = re.compile(r"[。.！？!?]")
QUOTE_RE = re.compile('["“”「」『』]')


def count_nonspace(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def strip_submission_front_matter(text: str) -> str:
    """Remove generated title/guide material before the first chapter."""
    lines = text.splitlines()
    first_chapter = None
    for index, line in enumerate(lines):
        if re.match(r"^\s*##\s*", line):
            first_chapter = index
            break
    if first_chapter is None:
        return text
    return "\n".join(lines[first_chapter:])


def rhythm_units(text: str) -> List[str]:
    body = strip_submission_front_matter(text)
    units: List[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("导语："):
            continue
        units.append(line)
    if len(units) >= 20:
        return units

    # Fallback for sources that are stored as long paragraphs.
    compact = re.sub(r"\s+", "", body)
    parts = [part.strip() for part in re.split(r"(?<=[。！？!?；;])", compact) if part.strip()]
    return [part for part in parts if not part.startswith("#")]


def compute_comma_period_ratio(text: str) -> float:
    """Ratio of commas (，,、) to periods (。.！？!?)."""
    commas = len(COMMA_RE.findall(text))
    periods = len(PERIOD_RE.findall(text))
    if periods == 0:
        return 0.0
    return round(commas / periods, 3)


def compute_sentence_avg_len(text: str) -> float:
    """Average sentence length (chars between sentence-end punctuation)."""
    compact = re.sub(r"\s+", "", text)
    sentences = [s for s in SENTENCE_END_RE.split(compact) if s.strip()]
    if not sentences:
        return 0.0
    return round(sum(len(s) for s in sentences) / len(sentences), 1)


def rhythm_profile(text: str) -> Dict[str, Any]:
    units = rhythm_units(text)
    lengths = [count_nonspace(unit) for unit in units if count_nonspace(unit) > 0]
    chars = count_nonspace("\n".join(units))
    question_marks = text.count("？") + text.count("?")
    comma_period_ratio = compute_comma_period_ratio(text)
    sentence_avg_len = compute_sentence_avg_len(text)
    if not lengths:
        return {
            "chars": chars,
            "line_count": 0,
            "avg_line_chars": 0.0,
            "median_line_chars": 0.0,
            "short_line_rate": 0.0,
            "long_line_rate": 0.0,
            "quote_line_rate": 0.0,
            "barrage_line_rate": 0.0,
            "question_marks_per_k": 0.0,
            "comma_period_ratio": comma_period_ratio,
            "sentence_avg_len": sentence_avg_len,
        }
    return {
        "chars": chars,
        "line_count": len(lengths),
        "avg_line_chars": round(sum(lengths) / len(lengths), 3),
        "median_line_chars": round(float(statistics.median(lengths)), 3),
        "short_line_rate": round(sum(1 for value in lengths if value <= 16) / len(lengths), 4),
        "long_line_rate": round(sum(1 for value in lengths if value >= 40) / len(lengths), 4),
        "quote_line_rate": round(sum(1 for unit in units if QUOTE_RE.search(unit)) / len(units), 4),
        "barrage_line_rate": round(sum(1 for unit in units if unit.startswith("【")) / len(units), 4),
        "question_marks_per_k": round(question_marks / max(chars / 1000, 1e-6), 3),
        "comma_period_ratio": comma_period_ratio,
        "sentence_avg_len": sentence_avg_len,
    }


def rhythm_fit(source_text: str, candidate_text: str) -> Dict[str, Any]:
    source = rhythm_profile(source_text)
    candidate = rhythm_profile(candidate_text)
    applicable = source["chars"] >= 2500 and source["line_count"] >= 50 and candidate["chars"] >= 3000
    failures: List[str] = []

    if applicable:
        src_avg = float(source["avg_line_chars"])
        cand_avg = float(candidate["avg_line_chars"])
        if src_avg and src_avg <= 25:
            ceiling = max(src_avg * 1.25, src_avg + 3.5)
            if cand_avg > ceiling:
                failures.append(
                    f"avg_line_chars {cand_avg:.2f} exceeds source-fast ceiling {ceiling:.2f}"
                )
        if src_avg >= 10:
            floor = src_avg * 0.78
            if cand_avg < floor:
                failures.append(
                    f"avg_line_chars {cand_avg:.2f} below source-rhythm floor {floor:.2f}"
                )

        src_short = float(source["short_line_rate"])
        cand_short = float(candidate["short_line_rate"])
        if src_short >= 0.40 and cand_short < src_short * 0.60:
            failures.append(
                f"short_line_rate {cand_short:.3f} below source-fit floor {src_short * 0.60:.3f}"
            )
        if src_short <= 0.75 and cand_short > min(0.88, src_short + 0.14):
            failures.append(
                f"short_line_rate {cand_short:.3f} over-fragments source rhythm {src_short:.3f}"
            )

        src_long = float(source.get("long_line_rate", 0))
        cand_long = float(candidate.get("long_line_rate", 0))
        long_ceiling = max(src_long * 2.0, 0.20)
        if cand_long > long_ceiling:
            failures.append(
                f"long_line_rate {cand_long:.3f} exceeds ceiling {long_ceiling:.3f} "
                f"(source {src_long:.3f})"
            )

        src_quote = float(source["quote_line_rate"])
        cand_quote = float(candidate["quote_line_rate"])
        if src_quote >= 0.20 and cand_quote < src_quote * 0.35 and (src_quote - cand_quote) >= 0.12:
            failures.append(
                f"quote_line_rate {cand_quote:.3f} collapses from source {src_quote:.3f}"
            )
        if src_quote >= 0.10 and cand_quote > max(src_quote * 1.55, src_quote + 0.12):
            failures.append(
                f"quote_line_rate {cand_quote:.3f} over-cranks dialogue from source {src_quote:.3f}"
            )

        src_barrage = float(source.get("barrage_line_rate", 0.0))
        cand_barrage = float(candidate.get("barrage_line_rate", 0.0))
        if src_barrage >= 0.10 and cand_barrage < src_barrage * 0.45:
            failures.append(
                f"barrage_line_rate {cand_barrage:.3f} below source-fit floor {src_barrage * 0.45:.3f}"
            )
        if src_barrage >= 0.10 and cand_barrage > src_barrage * 1.8:
            failures.append(
                f"barrage_line_rate {cand_barrage:.3f} overuses barrage from source {src_barrage:.3f}"
            )

        src_q = float(source["question_marks_per_k"])
        cand_q = float(candidate["question_marks_per_k"])
        if src_q >= 1.0 and cand_q < src_q * 0.35:
            failures.append(
                f"question_marks_per_k {cand_q:.2f} below source-fit floor {src_q * 0.35:.2f}"
            )
        if src_q >= 1.0 and cand_q > src_q * 1.55:
            failures.append(
                f"question_marks_per_k {cand_q:.2f} over-cranks question pressure from source {src_q:.2f}"
            )

    return {
        "status": "pass" if not failures else "fail",
        "applicable": applicable,
        "source": source,
        "candidate": candidate,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    source = Path(args.source).read_text(encoding="utf-8")
    candidate = Path(args.candidate).read_text(encoding="utf-8")
    result = rhythm_fit(source, candidate)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            "status={status} source_avg={sa} candidate_avg={ca} "
            "source_short={ss} candidate_short={cs} source_quote={sq} candidate_quote={cq} "
            "source_barrage={sb} candidate_barrage={cb}".format(
                status=result["status"],
                sa=result["source"]["avg_line_chars"],
                ca=result["candidate"]["avg_line_chars"],
                ss=result["source"]["short_line_rate"],
                cs=result["candidate"]["short_line_rate"],
                sq=result["source"]["quote_line_rate"],
                cq=result["candidate"]["quote_line_rate"],
                sb=result["source"].get("barrage_line_rate", 0),
                cb=result["candidate"].get("barrage_line_rate", 0),
            )
        )
        for failure in result["failures"]:
            print(f"- {failure}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
