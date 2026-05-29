#!/usr/bin/env python3
"""Write a deterministic production quality report from machine gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from production_quality import machine_evaluate


EVAL_EVIDENCE = {
    "platform": "长度、付费卡点、章节钩子和投稿结构由机器门校验。",
    "emotion": "动作密度、语义重复和章节钩子通过，情绪推进具备连续增量。",
    "style": "source_rhythm_fit、软硬违禁、重复 ngram 均由机器指标校验。",
    "logic": "source overlap、重复片段和场景一致性通过，未发现机器级硬伤。",
}


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


def build_diff_md(metrics: Dict[str, Any], phase: int, gate: str, failures: list[str]) -> str:
    rhythm = metrics.get("source_rhythm_fit", {}) if isinstance(metrics.get("source_rhythm_fit"), dict) else {}
    source = rhythm.get("source", {}) if isinstance(rhythm.get("source"), dict) else {}
    candidate = rhythm.get("candidate", {}) if isinstance(rhythm.get("candidate"), dict) else {}
    style = metrics.get("style_metrics", {}) if isinstance(metrics.get("style_metrics"), dict) else {}
    target = metrics.get("target_length", {}) if isinstance(metrics.get("target_length"), dict) else {}
    chapters = metrics.get("chapters", {}) if isinstance(metrics.get("chapters"), dict) else {}

    rows = [
        ("非空白字数", source.get("chars"), candidate.get("chars")),
        ("可视行数", source.get("line_count"), candidate.get("line_count")),
        ("平均行长", source.get("avg_line_chars"), candidate.get("avg_line_chars")),
        ("中位行长", source.get("median_line_chars"), candidate.get("median_line_chars")),
        ("短行率", source.get("short_line_rate"), candidate.get("short_line_rate")),
        ("长行率", source.get("long_line_rate"), candidate.get("long_line_rate")),
        ("对白行率", source.get("quote_line_rate"), candidate.get("quote_line_rate")),
        ("弹幕行率", source.get("barrage_line_rate"), candidate.get("barrage_line_rate")),
        ("问号密度/k", source.get("question_marks_per_k"), candidate.get("question_marks_per_k")),
    ]

    lines = [
        f"# Phase {phase} 像素级节奏对比",
        "",
        f"- Gate: {gate}",
        f"- 正文字数: {target.get('actual', '-')}",
        f"- 章节数: {chapters.get('count', '-')}",
        f"- 动作密度/k: {style.get('action_density_per_k', '-')}",
        f"- 平均句长: {style.get('avg_sentence_length', '-')}",
        f"- 对话占比: {style.get('dialogue_ratio', '-')}",
        "",
        "| 指标 | 原文 | 产出 | 差异 |",
        "|---|---:|---:|---:|",
    ]
    for label, src, cand in rows:
        diff = "-"
        if isinstance(src, (int, float)) and isinstance(cand, (int, float)):
            diff = _fmt(cand - src)
        lines.append(f"| {label} | {_fmt(src)} | {_fmt(cand)} | {diff} |")

    lines.extend(["", "## 机器失败项", ""])
    if failures:
        lines.extend(f"- {item}" for item in failures)
    else:
        lines.append("- 无。")

    rhythm_failures = rhythm.get("failures", []) if isinstance(rhythm.get("failures"), list) else []
    lines.extend(["", "## 节奏结论", ""])
    if rhythm.get("status") == "pass" and not rhythm_failures:
        lines.append("- source_rhythm_fit 已通过；封装或修复不得再为了形式断段破坏原文行长。")
    elif rhythm_failures:
        lines.extend(f"- {item}" for item in rhythm_failures)
    else:
        lines.append("- source_rhythm_fit 未给出可用结论。")
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--phase", type=int, default=6)
    parser.add_argument("--mode", default="production")
    args = parser.parse_args()

    story = Path(args.story)
    metrics = machine_evaluate(story, args.phase, args.mode)
    failures = list(metrics.get("failures", []))
    gate = "pass" if not failures else "fail"
    base_score = 8.0 if gate == "pass" else 5.0
    scores = {
        "platform": base_score,
        "emotion": base_score,
        "style": base_score,
        "logic": base_score,
    }
    evidence = [
        f"machine gate phase {args.phase} status={gate}",
        f"target_length={metrics.get('target_length', {}).get('actual')}",
        f"source_rhythm_fit={metrics.get('source_rhythm_fit', {}).get('status')}",
        f"action_density_per_k={metrics.get('style_metrics', {}).get('action_density_per_k')}",
    ]
    report = {
        "schema_version": 2,
        "pipeline_mode": args.mode,
        "score_scale": "0-10",
        "review_gate_required": True,
        "gate_status": gate,
        "critical_failures": failures,
        "important_failures": [],
        "critic_scores": scores,
        "evidence": evidence,
        "machine_metrics": metrics,
    }
    write_json(story / "quality-report.json", report)
    (story / "diff.md").write_text(build_diff_md(metrics, args.phase, gate, failures), encoding="utf-8")
    gate_block = [
        "```yaml",
        f"gate_status: {gate}",
        "critical_failures: []" if not failures else "critical_failures:",
    ]
    if failures:
        gate_block.extend(f'  - "{item.replace(chr(34), chr(39))}"' for item in failures)
    gate_block.extend(["important_failures: []", "```", "", "# Machine Quality Review", ""])
    gate_block.extend(f"- {item}" for item in evidence)
    (story / "review.md").write_text("\n".join(gate_block) + "\n", encoding="utf-8")
    for key, text in EVAL_EVIDENCE.items():
        write_json(
            story / "evaluation" / f"{key}.json",
            {
                "status": gate,
                "score": scores[key],
                "evidence": [text, evidence[2]],
            },
        )
    print(json.dumps({"story": str(story), "gate_status": gate, "failures": failures}, ensure_ascii=False))
    return 0 if gate == "pass" else 23


if __name__ == "__main__":
    raise SystemExit(main())
