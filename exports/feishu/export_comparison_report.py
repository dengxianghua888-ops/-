#!/usr/bin/env python3
"""将 v5_part2_comparison_report.md 转换为飞书文档 XML 格式"""
from __future__ import annotations

import html
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
MD_PATH = OUT / "v5_part2_comparison_report.md"
XML_PATH = OUT / "batch_v5_part2_20260527.comparison_report.xml"


def esc(v: str) -> str:
    return html.escape(v, quote=True)


def md_table_to_xml(lines: list[str]) -> str:
    rows = []
    header_line = lines[0]
    cells = [c.strip() for c in header_line.strip().strip("|").split("|")]
    ncols = len(cells)
    col_width = max(60, 720 // ncols)
    cols = "".join(f'<col span="1" width="{col_width}"/>' for _ in range(ncols))
    colgroup = f"<colgroup>{cols}</colgroup>"
    header_row = "<tr>" + "".join(f'<th background-color="light-gray">{esc(c)}</th>' for c in cells) + "</tr>"

    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in cells) + "</tr>")

    return f"<table>{colgroup}<thead>{header_row}</thead><tbody>{''.join(rows)}</tbody></table>"


def convert(md_text: str) -> str:
    xml_parts = [
        '<title>短篇仿写终稿｜V5 第二批深度对比报告</title>',
        '<callout emoji="📊" background-color="light-blue" border-color="blue">',
        '<p>10 篇 v5 结构保真产线终稿与源文的多维度对比分析。批次：batch_v5_part2_20260527</p>',
        '</callout>',
    ]

    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped or stripped.startswith("> "):
            i += 1
            continue

        if stripped.startswith("# "):
            i += 1
            continue

        if stripped == "---":
            xml_parts.append("<hr/>")
            i += 1
            continue

        if stripped.startswith("## "):
            xml_parts.append(f"<h1>{esc(stripped[3:])}</h1>")
            i += 1
            continue

        if stripped.startswith("### "):
            xml_parts.append(f"<h2>{esc(stripped[4:])}</h2>")
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            xml_parts.append(md_table_to_xml(table_lines))
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            xml_parts.append("<ul>" + "".join(f"<li>{esc(it)}</li>" for it in items) + "</ul>")
            continue

        if re.match(r"^\d+\. ", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i].strip()):
                items.append(re.sub(r"^\d+\. ", "", lines[i].strip()))
                i += 1
            xml_parts.append("<ol>" + "".join(f"<li>{esc(it)}</li>" for it in items) + "</ol>")
            continue

        text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
        xml_parts.append(f"<p>{esc(text)}</p>")
        i += 1

    return "\n".join(xml_parts)


if __name__ == "__main__":
    md_text = MD_PATH.read_text(encoding="utf-8")
    xml = convert(md_text)
    XML_PATH.write_text(xml + "\n", encoding="utf-8")
    print(f"Report XML written: {XML_PATH}")
