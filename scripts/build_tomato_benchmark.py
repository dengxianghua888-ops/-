#!/usr/bin/env python3
"""Aggregate quality-report.json metrics from existing production stories into
context/tomato-benchmark.json.

The benchmark is used by tomato-rubric-score.py as a reference distribution.
Only stories whose quality-report.json reports gate_status=pass are aggregated.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
STORIES_DIR = ROOT / "stories"
OUT_PATH = ROOT / "context" / "tomato-benchmark.json"


def quantiles(values: List[float]) -> Dict[str, float]:
    if not values:
        return {"p10": 0.0, "p50": 0.0, "p90": 0.0, "mean": 0.0, "stdev": 0.0}
    sorted_values = sorted(values)
    n = len(sorted_values)

    def pick(p: float) -> float:
        index = max(0, min(n - 1, int(round((n - 1) * p))))
        return float(sorted_values[index])

    return {
        "p10": round(pick(0.10), 4),
        "p50": round(pick(0.50), 4),
        "p90": round(pick(0.90), 4),
        "mean": round(statistics.fmean(values), 4),
        "stdev": round(statistics.pstdev(values), 4) if n > 1 else 0.0,
    }


def collect() -> Dict[str, Any]:
    samples: List[Dict[str, Any]] = []
    for story in sorted(STORIES_DIR.iterdir()):
        if not story.is_dir():
            continue
        report = story / "quality-report.json"
        if not report.exists():
            continue
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if str(data.get("gate_status", "")).lower() != "pass":
            continue
        metrics = data.get("machine_metrics", {})
        chapters = metrics.get("chapters", {}) or {}
        style = metrics.get("style_metrics", {}) or {}
        target = metrics.get("target_length", {}) or {}
        paywall = metrics.get("paywall_cards", {}) or {}
        sample = {
            "slug": story.name,
            "total_chars": int(target.get("actual", 0) or 0),
            "chapter_count": int(chapters.get("count", 0) or 0),
            "chapter_lengths": list(chapters.get("lengths", []) or []),
            "hook_coverage": float(chapters.get("hook_coverage", 0.0) or 0.0),
            "paywall_actual": int(paywall.get("actual", 0) or 0),
            "avg_sentence_length": float(style.get("avg_sentence_length", 0.0) or 0.0),
            "action_density_per_k": float(style.get("action_density_per_k", 0.0) or 0.0),
            "physical_emotion_total": sum(
                int(value or 0) for value in (style.get("physical_emotion_hits", {}) or {}).values()
            ),
            "soft_forbidden_total": sum(
                int(value or 0) for value in (style.get("soft_forbidden_hits", {}) or {}).values()
            ),
            "critic_scores": data.get("critic_scores", {}),
        }
        if sample["total_chars"] and sample["chapter_count"]:
            samples.append(sample)
    return build_benchmark(samples)


def build_benchmark(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not samples:
        return {"sample_count": 0, "samples": []}

    total_chars = [s["total_chars"] for s in samples]
    chapter_counts = [s["chapter_count"] for s in samples]
    hook_cov = [s["hook_coverage"] for s in samples]
    paywall = [s["paywall_actual"] for s in samples]
    avg_sl = [s["avg_sentence_length"] for s in samples if s["avg_sentence_length"]]
    action = [s["action_density_per_k"] for s in samples if s["action_density_per_k"]]
    phys = [s["physical_emotion_total"] for s in samples]
    soft_f = [s["soft_forbidden_total"] for s in samples]

    chapter_length_pool: List[float] = []
    for s in samples:
        chapter_length_pool.extend(float(x) for x in s["chapter_lengths"])

    chapter_stdev_pool = []
    for s in samples:
        if len(s["chapter_lengths"]) > 1:
            chapter_stdev_pool.append(statistics.pstdev(s["chapter_lengths"]))

    return {
        "sample_count": len(samples),
        "generated_from": [s["slug"] for s in samples],
        "total_chars": quantiles(total_chars),
        "chapter_count": quantiles(chapter_counts),
        "chapter_length": quantiles(chapter_length_pool),
        "chapter_length_stdev_per_story": quantiles(chapter_stdev_pool),
        "hook_coverage": quantiles(hook_cov),
        "paywall_actual": quantiles(paywall),
        "avg_sentence_length": quantiles(avg_sl),
        "action_density_per_k": quantiles(action),
        "physical_emotion_total": quantiles(phys),
        "soft_forbidden_total": quantiles(soft_f),
    }


def main() -> int:
    benchmark = collect()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {OUT_PATH} with {benchmark.get('sample_count', 0)} samples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
