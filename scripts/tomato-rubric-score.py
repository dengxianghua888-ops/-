#!/usr/bin/env python3
"""Score a finished production story against the tomato hot-sample benchmark.

Each dimension scores 0-10. The story passes when ``overall_score >=
pass_threshold``. Below threshold, ``rework_targets`` lists scenes / chapters
that contributed most to the gap so storyforge can do targeted reruns instead
of full pipeline restarts.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List

from rhythm_metrics import rhythm_fit

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_PATH = ROOT / "context" / "tomato-benchmark.json"


def _score_distance(value: float, ref: Dict[str, float]) -> float:
    """Map distance from p10..p90 band to a 0-10 score.

    Inside band -> 10. Each stdev outside loses 2 points, floor at 0.
    """
    p10 = ref.get("p10", 0.0)
    p90 = ref.get("p90", 0.0)
    stdev = max(ref.get("stdev", 0.0), 1e-6)
    if value == 0 and ref.get("mean", 0.0) > 0:
        # Strong fail when story has zero where benchmark has signal.
        return max(0.0, 10.0 - 6.0)
    if p10 <= value <= p90:
        return 10.0
    if value < p10:
        gap = (p10 - value) / stdev
    else:
        gap = (value - p90) / stdev
    return max(0.0, round(10.0 - gap * 2.0, 2))


def _load_metrics(story: Path) -> Dict[str, Any]:
    report_path = story / "quality-report.json"
    if not report_path.exists():
        raise ValueError(f"missing quality-report.json under {story}")
    return json.loads(report_path.read_text(encoding="utf-8")).get("machine_metrics", {})


def _chapter_text(story: Path) -> List[str]:
    chapters_dir = story / "final-chapters"
    if not chapters_dir.is_dir():
        return []
    out: List[str] = []
    for path in sorted(chapters_dir.glob("ch*.md")):
        body = "\n".join(l for l in path.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))
        out.append(body.strip())
    return out


def _hook_density_score(chapters: List[str]) -> Dict[str, Any]:
    if not chapters:
        return {"score": 0.0, "evidence": "no chapters"}
    weak: List[str] = []
    strong = 0
    for idx, ch in enumerate(chapters, 1):
        last_lines = [l for l in ch.splitlines() if l.strip()]
        if not last_lines:
            weak.append(f"ch{idx:02d}")
            continue
        last = last_lines[-1].strip()
        # Heuristic: a strong hook ends with sentence punctuation, including
        # punctuation inside Chinese quotes / brackets used by dialogue and
        # barrage-style lines.
        has_punct = bool(re.search(r"[。！？!?](?:[”」』】）)]*)$", last))
        has_signal = bool(re.search(r"[“”「」『』【】：:]", last)) or len(last) >= 12
        if has_punct and has_signal:
            strong += 1
        else:
            weak.append(f"ch{idx:02d}")
    score = round(10.0 * strong / max(len(chapters), 1), 2)
    return {"score": score, "evidence": f"{strong}/{len(chapters)} 强钩,弱钩章: {','.join(weak) if weak else '无'}", "weak_chapters": weak}


def _paywall_layout_score(metrics: Dict[str, Any], total_chars: int) -> Dict[str, Any]:
    paywall_actual = int(metrics.get("paywall_cards", {}).get("actual", 0) or 0)
    required = int(metrics.get("paywall_cards", {}).get("required", 4) or 4)
    if paywall_actual >= required:
        # Bonus for hitting target without spamming
        ratio = paywall_actual / max(required, 1)
        score = 10.0 if ratio <= 2.5 else max(0.0, 10.0 - (ratio - 2.5) * 1.5)
        return {"score": round(score, 2), "evidence": f"付费卡点 {paywall_actual}/{required}"}
    return {"score": round(10.0 * paywall_actual / max(required, 1), 2), "evidence": f"付费卡点不足: {paywall_actual}/{required}"}


def _mobile_readability_score(metrics: Dict[str, Any]) -> Dict[str, Any]:
    direct = metrics.get("direct_submission", {}) or {}
    mobile = direct.get("mobile_paragraphs", {}) or {}
    offending = int(mobile.get("offending_paragraphs", 0) or 0)
    if offending == 0:
        return {"score": 10.0, "evidence": "全部段落单句"}
    score = max(0.0, round(10.0 - offending * 0.5, 2))
    return {"score": score, "evidence": f"{offending} 段违规"}


def _length_alignment_score(metrics: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
    target = metrics.get("target_length", {}) or {}
    chapters = metrics.get("chapters", {}) or {}
    actual = float(target.get("actual", 0) or 0)
    chapter_lengths = chapters.get("lengths") or []

    score_total = _score_distance(actual, benchmark.get("total_chars", {}))
    if chapter_lengths and len(chapter_lengths) > 1:
        story_stdev = statistics.pstdev(chapter_lengths)
    else:
        story_stdev = 0.0
    score_stdev = _score_distance(story_stdev, benchmark.get("chapter_length_stdev_per_story", {}))
    final_score = round(0.6 * score_total + 0.4 * score_stdev, 2)
    return {
        "score": final_score,
        "evidence": f"总字数 {actual:.0f},章节方差 {story_stdev:.1f}",
    }


def _action_density_score(metrics: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
    style = metrics.get("style_metrics", {}) or {}
    density = float(style.get("action_density_per_k", 0.0) or 0.0)
    score = _score_distance(density, benchmark.get("action_density_per_k", {}))
    return {"score": score, "evidence": f"动作密度 {density}/k"}


def _style_signature_score(metrics: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
    style = metrics.get("style_metrics", {}) or {}
    asl = float(style.get("avg_sentence_length", 0.0) or 0.0)
    soft = sum(int(v or 0) for v in (style.get("soft_forbidden_hits", {}) or {}).values())
    hard = sum(int(v or 0) for v in (style.get("forbidden_hits", {}) or {}).values())
    asl_score = _score_distance(asl, benchmark.get("avg_sentence_length", {}))
    soft_penalty = min(4.0, soft * 0.5)
    hard_penalty = min(8.0, hard * 2.0)
    final = max(0.0, round(asl_score - soft_penalty - hard_penalty, 2))
    return {"score": final, "evidence": f"平均句长 {asl},软违禁 {soft} 次,硬违禁 {hard} 次"}


def _source_rhythm_fit_score(story: Path) -> Dict[str, Any]:
    source_path = story / "source.md"
    final_path = story / "final.md"
    if not source_path.exists() or not final_path.exists():
        return {"score": 10.0, "evidence": "未发现可比源文或终稿,跳过源节奏比对"}
    result = rhythm_fit(
        source_path.read_text(encoding="utf-8"),
        final_path.read_text(encoding="utf-8"),
    )
    if not result.get("applicable"):
        return {"score": 10.0, "evidence": "源文规模不足以稳定计算节奏,跳过硬扣分"}
    source = result["source"]
    candidate = result["candidate"]
    penalties = 0.0
    if result["failures"]:
        penalties += min(6.0, len(result["failures"]) * 2.0)
    avg_gap = abs(float(candidate["avg_line_chars"]) - float(source["avg_line_chars"]))
    penalties += min(2.0, avg_gap / 8.0)
    quote_gap = max(0.0, float(source["quote_line_rate"]) - float(candidate["quote_line_rate"]))
    penalties += min(2.0, quote_gap * 4.0)
    score = max(0.0, round(10.0 - penalties, 2))
    evidence = (
        f"源/稿均行长 {source['avg_line_chars']}/{candidate['avg_line_chars']}, "
        f"短行率 {source['short_line_rate']}/{candidate['short_line_rate']}, "
        f"对白行率 {source['quote_line_rate']}/{candidate['quote_line_rate']}"
    )
    if result["failures"]:
        evidence += "; " + "；".join(result["failures"])
    return {"score": score, "evidence": evidence, "details": result}


def score_story(story: Path, benchmark: Dict[str, Any]) -> Dict[str, Any]:
    metrics = _load_metrics(story)
    chapters = _chapter_text(story)
    total_chars = int(metrics.get("target_length", {}).get("actual", 0) or 0)

    dims = {
        "length_alignment": _length_alignment_score(metrics, benchmark),
        "hook_density": _hook_density_score(chapters),
        "paywall_layout": _paywall_layout_score(metrics, total_chars),
        "action_density": _action_density_score(metrics, benchmark),
        "style_signature": _style_signature_score(metrics, benchmark),
        "source_rhythm_fit": _source_rhythm_fit_score(story),
        "mobile_readability": _mobile_readability_score(metrics),
    }
    weights = {
        "length_alignment": 0.08,
        "hook_density": 0.18,
        "paywall_layout": 0.08,
        "action_density": 0.12,
        "style_signature": 0.14,
        "source_rhythm_fit": 0.30,
        "mobile_readability": 0.10,
    }
    overall = round(sum(dims[k]["score"] * weights[k] for k in dims), 2)
    if dims["source_rhythm_fit"]["score"] < 7.0:
        # Rhythm fidelity is the anti-padding gate. A story cannot pass Tomato
        # imitation review by averaging away a source-rhythm collapse.
        overall = min(overall, 6.99)
    rework: List[str] = []
    for name, value in dims.items():
        if value["score"] < 7.0:
            if name == "hook_density":
                rework.extend(value.get("weak_chapters", []))
            elif name == "source_rhythm_fit":
                rework.append("source_rhythm_fit")
    return {
        "story": str(story),
        "overall_score": overall,
        "dimensions": dims,
        "rework_targets": sorted(set(rework)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--threshold", type=float, default=8.0)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not BENCHMARK_PATH.exists():
        print(
            f"benchmark missing: {BENCHMARK_PATH}; run scripts/build_tomato_benchmark.py first",
            file=sys.stderr,
        )
        return 11
    benchmark = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))

    story = Path(args.story)
    try:
        result = score_story(story, benchmark)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 11

    result["pass_threshold"] = args.threshold
    result["status"] = "pass" if result["overall_score"] >= args.threshold else "fail"

    if args.write_report:
        out_path = story / "tomato-rubric.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"overall={result['overall_score']} status={result['status']} threshold={args.threshold}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
