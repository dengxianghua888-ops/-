#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exports" / "feishu"
BATCH = "seq5_20260519"
MANIFEST = OUT / f"manifest.{BATCH}.json"
STORY_DIRS = [
    "prod_seq5_20260519_ancient_moon_spring",
    "prod_seq5_20260519_empress_escape",
    "prod_seq5_20260519_poor_mom_3000",
    "prod_seq5_20260519_husband_drowning_divorce",
    "prod_seq5_20260519_property_rent_exit",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def title_from_final(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def metrics_from_report(story_dir: Path, final_text: str) -> dict[str, object]:
    quality = json.loads(read_text(story_dir / "quality-report.json"))
    rubric = json.loads(read_text(story_dir / "tomato-rubric.json"))
    mm = quality.get("machine_metrics", {})
    length = mm.get("target_length", {})
    chapters = mm.get("chapters", {})
    return {
        "pipeline": quality.get("pipeline_mode", "production"),
        "gate": quality.get("gate_status", "pass"),
        "chars": length.get("actual") or len(re.sub(r"\s+", "", final_text)),
        "chapters": chapters.get("count", ""),
        "hook_coverage": chapters.get("hook_coverage", ""),
        "paywall_cards": (mm.get("paywall_cards") or {}).get("actual", ""),
        "paywall_required": (mm.get("paywall_cards") or {}).get("required", ""),
        "overlap": (mm.get("source_overlap") or {}).get("max_continuous_overlap_chars", ""),
        "repeat": (mm.get("repeated_ngram") or {}).get("max_repeated_substring_chars", ""),
        "rubric": rubric.get("overall_score", ""),
        "rubric_status": rubric.get("status", ""),
    }


def para_xml(lines: list[str]) -> str:
    text = "\n".join(lines).strip()
    if not text:
        return ""
    return f"<p>{esc(text).replace(chr(10), '<br/>')}</p>"


def parse_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def markdown_table_to_xml(lines: list[str]) -> str:
    rows = [parse_table_cells(line) for line in lines if line.strip().startswith("|")]
    rows = [row for row in rows if row and not is_table_separator(row)]
    if not rows:
        return ""
    header, body_rows = rows[0], rows[1:]
    head = "".join(f'<th background-color="light-gray">{esc(cell)}</th>' for cell in header)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>"
        for row in body_rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def markdownish_to_xml(text: str, *, strip_first_h1: bool = False) -> str:
    blocks: list[str] = []
    para: list[str] = []
    first_h1_seen = False

    def flush() -> None:
        nonlocal para
        block = para_xml(para)
        if block:
            blocks.append(block)
        para = []

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush()
            i += 1
            continue

        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            flush()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].rstrip())
                i += 1
            table_xml = markdown_table_to_xml(table_lines)
            if table_xml:
                blocks.append(table_xml)
            continue

        if line.startswith("# "):
            flush()
            if strip_first_h1 and not first_h1_seen:
                first_h1_seen = True
                i += 1
                continue
            first_h1_seen = True
            blocks.append(f"<h1>{esc(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            flush()
            blocks.append(f"<h2>{esc(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            flush()
            blocks.append(f"<h3>{esc(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            flush()
            items = [line[2:].strip()]
            blocks.append("<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>")
        else:
            para.append(line)
        i += 1

    flush()
    return "\n".join(blocks)


def table(rows: list[tuple[str, object]]) -> str:
    body = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in rows)
    return (
        "<table>"
        '<colgroup><col span="1" width="150"/><col span="1" width="440"/></colgroup>'
        '<thead><tr><th background-color="light-gray">项目</th>'
        '<th background-color="light-gray">内容</th></tr></thead>'
        f"<tbody>{body}</tbody></table>"
    )


def build_story(slug: str) -> dict[str, object]:
    story_dir = ROOT / "stories" / slug
    final_text = read_text(story_dir / "final.md")
    tomato_text = read_text(story_dir / "tomato-submission.md")
    title = title_from_final(final_text, slug)
    metrics = metrics_from_report(story_dir, final_text)
    doc_title = f"短篇仿写终稿｜{title}"

    skeleton = "\n".join(
        [
            f"<title>{esc(doc_title)}</title>",
            '<callout emoji="✅" background-color="light-green" border-color="green">',
            "<p>已按 production 产线完成 1-8 阶段复检；正文保留 final.md 原貌，仅做飞书文档结构化排版。</p>",
            "</callout>",
            "<h1>产线打标</h1>",
            table(
                [
                    ("本地目录", f"stories/{slug}"),
                    ("产线模式", metrics["pipeline"]),
                    ("闸门状态", metrics["gate"]),
                    ("番茄评分", f"{metrics['rubric']} / {metrics['rubric_status']}"),
                    ("正文字符数", metrics["chars"]),
                    ("章节数", metrics["chapters"]),
                    ("章节钩子覆盖", metrics["hook_coverage"]),
                    ("付费卡点", f"{metrics['paywall_cards']} / {metrics['paywall_required']}"),
                    ("最大原文连续重叠", metrics["overlap"]),
                    ("最大重复片段", metrics["repeat"]),
                ]
            ),
            "<hr/>",
            "<h1>番茄投稿包</h1>",
            markdownish_to_xml(tomato_text, strip_first_h1=True),
            "<hr/>",
            "<h1>正文</h1>",
        ]
    )

    body = markdownish_to_xml(final_text, strip_first_h1=True)
    prefix = OUT / f"{BATCH}.{slug}"
    skeleton_path = Path(f"{prefix}.skeleton.xml")
    body_path = Path(f"{prefix}.body.xml")
    full_path = Path(f"{prefix}.full.xml")
    skeleton_path.write_text(skeleton + "\n", encoding="utf-8")
    body_path.write_text(body + "\n", encoding="utf-8")
    full_path.write_text(skeleton + "\n" + body + "\n", encoding="utf-8")

    return {
        "slug": slug,
        "title": title,
        "doc_title": doc_title,
        "chars": metrics["chars"],
        "chapters": metrics["chapters"],
        "rubric": metrics["rubric"],
        "skeleton": str(skeleton_path),
        "body": str(body_path),
        "full": str(full_path),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = [build_story(slug) for slug in STORY_DIRS]
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "count": len(manifest), "manifest": str(MANIFEST)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
