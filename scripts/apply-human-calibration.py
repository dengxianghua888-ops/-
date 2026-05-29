#!/usr/bin/env python3
"""Apply an approved human calibration decision to V4 corpus artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from v4_quality import CALIBRATION_GENE_FIELDS, load_human_calibration

V4_ARTIFACTS = [
    "analysis/soul-contract.md",
    "analysis/reader-engine.md",
    "analysis/tension-ledger.md",
    "analysis/platform-fit.md",
]


def upsert_metadata(text: str, calibration: dict) -> str:
    replacements = {
        "v4_calibration_status": "human_calibrated",
        "v4_human_reviewer": calibration["v4_human_reviewer"],
        "v4_human_reviewed_at": calibration["v4_human_reviewed_at"],
    }
    for key, value in replacements.items():
        pattern = rf"^\*\*{re.escape(key)}\*\*:\s*.*$"
        line = f"**{key}**: {value}"
        if re.search(pattern, text, re.MULTILINE):
            text = re.sub(pattern, line, text, count=1, flags=re.MULTILINE)
        else:
            text = f"{line}\n{text}"
    return text


def replace_marked_value(text: str, label: str, value) -> str:
    pattern = rf"^(\*\*{re.escape(label)}\*\*[:：]\s*).*$"
    repl = rf"\g<1>{value}"
    return re.sub(pattern, repl, text, count=1, flags=re.MULTILINE)


def upsert_calibration_block(text: str, calibration: dict) -> str:
    start = "<!-- V4_HUMAN_CALIBRATION_START -->"
    end = "<!-- V4_HUMAN_CALIBRATION_END -->"
    block_lines = [
        start,
        "## 人工校准爆款基因",
        "",
    ]
    for key in CALIBRATION_GENE_FIELDS:
        block_lines.append(f"- **{key}**: {calibration[key]}")
    block_lines.extend([
        f"- **v4_human_reviewer**: {calibration['v4_human_reviewer']}",
        f"- **v4_human_reviewed_at**: {calibration['v4_human_reviewed_at']}",
        end,
    ])
    block = "\n".join(block_lines) + "\n\n"
    text = re.sub(rf"{re.escape(start)}.*?{re.escape(end)}\n*", "", text, flags=re.DOTALL)
    insert_at = 0
    title = re.search(r"^# .*\n+", text, re.MULTILINE)
    if title:
        insert_at = title.end()
    return text[:insert_at] + block + text[insert_at:]


def apply_calibrated_values(rel: str, text: str, calibration: dict) -> str:
    text = text.replace("V4 machine draft", "V4 human calibrated")
    text = text.replace(
        "machine_draft 仅从 V3 dissection 反推读者心理,需人工逐 Beat 校准。",
        "human_calibrated 已写入人工校准基因；逐 Beat 细节仍可由真人复核。",
    )
    if rel == "analysis/soul-contract.md":
        text = replace_marked_value(text, "一句话承诺", calibration["reader_promise"])
        text = replace_marked_value(text, "情绪债", calibration["emotional_debt_type"])
        text = replace_marked_value(text, "反派必须被惩罚的理由", calibration["antagonist_violation"])
        text = replace_marked_value(text, "核心姿态", calibration["protagonist_stance"])
        text = replace_marked_value(text, "最终必须兑现的体验", calibration["payoff_pattern"])
    elif rel == "analysis/reader-engine.md":
        text = replace_marked_value(text, "主要爽点", calibration["dominant_s爽点"])
    elif rel == "analysis/platform-fit.md":
        text = replace_marked_value(text, "总分", calibration["tomato_fit_score"])
    return upsert_calibration_block(text, calibration)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=str(Path(__file__).resolve().parent.parent / "corpus"))
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()

    slug_dir = Path(args.corpus) / args.slug
    try:
        calibration = load_human_calibration(slug_dir, require_approved=True)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    updated = 0
    for rel in V4_ARTIFACTS:
        path = slug_dir / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = upsert_metadata(text, calibration)
        text = apply_calibrated_values(rel, text, calibration)
        path.write_text(text, encoding="utf-8")
        updated += 1

    if updated == 0:
        print("no V4 artifacts found to update", file=sys.stderr)
        return 1

    print(
        f"applied human calibration: slug={args.slug} "
        f"reviewer={calibration['v4_human_reviewer']} artifacts={updated}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
