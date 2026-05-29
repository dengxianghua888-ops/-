#!/usr/bin/env python3
"""Diagnostic tool for dialogue quality analysis.

Outputs dialogue-diagnosis.json with advisory findings (not a gate).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

NARRATION_CRUTCH_RE = re.compile(r'(她|他)(知道|明白|意识到|清楚|心想|暗忖|终于明白|这才知道)')
CONFIRMATION_RE = re.compile(r'[““][^””]*你是说[^””]*[？?][“”]')
CONFIRMATION_REPLY_RE = re.compile(r'[““](对|没错|就是|是的|嗯)[，。,.][“”]')
QUOTE_LINE_RE = re.compile(r'["“”「『」』]')


def split_chapters(text: str) -> list[tuple[str, str]]:
    chapters = []
    current_title = ""
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current_lines:
                chapters.append((current_title, "\n".join(current_lines)))
            current_title = line[3:].strip()
            current_lines = []
        elif not line.startswith("# "):
            current_lines.append(line)
    if current_lines:
        chapters.append((current_title, "\n".join(current_lines)))
    return chapters


def quote_line_rate(text: str) -> float:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return 0.0
    quoted = sum(1 for l in lines if QUOTE_LINE_RE.search(l))
    return round(quoted / len(lines), 4)


def count_narration_crutches(text: str) -> list[dict]:
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in NARRATION_CRUTCH_RE.finditer(line):
            hits.append({"line": i, "match": m.group()})
    return hits


def detect_confirmation_dialogue(text: str) -> list[dict]:
    hits = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if CONFIRMATION_RE.search(line):
            if i + 1 < len(lines) and CONFIRMATION_REPLY_RE.search(lines[i + 1]):
                hits.append({"line": i + 1, "question": line.strip(), "reply": lines[i + 1].strip()})
    return hits


def diagnose(draft_path: Path, beat_bible_path: Path | None) -> dict:
    text = draft_path.read_text(encoding="utf-8")
    chapters = split_chapters(text)

    climax_beats: set[int] = set()
    if beat_bible_path and beat_bible_path.exists():
        bible = json.loads(beat_bible_path.read_text(encoding="utf-8"))
        for i, beat in enumerate(bible.get("beats", [])):
            if beat.get("is_climax_beat") or beat.get("paywall_card") or "climax" in str(beat.get("budget_role", "")).lower():
                climax_beats.add(i)

    chapter_stats = []
    for idx, (title, body) in enumerate(chapters):
        chapter_stats.append({
            "chapter": idx + 1,
            "title": title,
            "quote_line_rate": quote_line_rate(body),
            "is_climax": idx in climax_beats,
        })

    climax_rates = [c["quote_line_rate"] for c in chapter_stats if c["is_climax"]]
    non_climax_rates = [c["quote_line_rate"] for c in chapter_stats if not c["is_climax"]]

    avg_climax = sum(climax_rates) / len(climax_rates) if climax_rates else 0
    avg_non_climax = sum(non_climax_rates) / len(non_climax_rates) if non_climax_rates else 0

    crutches = count_narration_crutches(text)
    confirmations = detect_confirmation_dialogue(text)

    return {
        "draft": str(draft_path),
        "chapter_dialogue_distribution": chapter_stats,
        "summary": {
            "avg_climax_quote_rate": round(avg_climax, 4),
            "avg_non_climax_quote_rate": round(avg_non_climax, 4),
            "variance_ratio": round(avg_climax / avg_non_climax, 2) if avg_non_climax > 0 else None,
            "narration_crutches_count": len(crutches),
            "confirmation_dialogues_count": len(confirmations),
        },
        "narration_crutches": crutches[:10],
        "confirmation_dialogues": confirmations[:5],
        "advisory": _build_advisory(len(crutches), len(confirmations), avg_climax, avg_non_climax),
    }


def _build_advisory(crutch_count: int, confirm_count: int, climax_rate: float, non_climax_rate: float) -> list[str]:
    notes = []
    if crutch_count > 5:
        notes.append(f"叙述拐杖词 {crutch_count} 处(建议≤5)，考虑用动作/对话替代部分认知动词")
    if confirm_count > 0:
        notes.append(f"检测到 {confirm_count} 处信息确认型对话，建议改为权力位移式对话")
    if climax_rate > 0 and non_climax_rate > 0:
        ratio = climax_rate / non_climax_rate
        if ratio < 1.2:
            notes.append(f"高潮段与非高潮段对话密度差异不足(比值{ratio:.2f}，建议≥1.2)")
    return notes


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <draft.md> [beat-bible.json]", file=sys.stderr)
        return 1
    draft_path = Path(sys.argv[1])
    beat_bible_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = diagnose(draft_path, beat_bible_path)
    output_path = draft_path.parent / "dialogue-diagnosis.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    if result["advisory"]:
        print("\nAdvisory:")
        for note in result["advisory"]:
            print(f"  - {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
