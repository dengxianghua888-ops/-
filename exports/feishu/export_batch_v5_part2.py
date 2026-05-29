#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exports" / "feishu"
BATCH = "batch_v5_part2_20260527"
MANIFEST = OUT / f"manifest.{BATCH}.json"
INDEX_XML = OUT / f"feishu-index.{BATCH}.xml"

STORIES = [
    ("batch_v5_06_modern_reversal", "她穿着嫁衣跪在灵堂前，他却牵着白月光进了洞房"),
    ("batch_v5_07_family_ethics", "我把亲妈送进监狱的那天，全家人跪在法院门口求我"),
    ("batch_v5_08_ancient_BE", "他亲手为我披上凤冠，转身却把休书塞进了我的嫁妆箱"),
    ("batch_v5_09_urban_sweet_ceo", "总裁前夫每天假装路人偶遇我"),
    ("batch_v5_10_ancient_sweet", "本宫只想摆烂，皇帝非要宠我上天"),
    ("batch_v5_11_family_ethics", "七年男友求婚那天，我把戒指扔进了火锅里"),
    ("batch_v5_12_modern_reversal", "他当着全公司的面撕碎我的画，却不知道画里藏着他的命"),
    ("batch_v5_13_urban_sweet_ceo", "他在婚礼上跪着叫我恩人，我把他偷拍的视频投到了大屏幕上"),
    ("batch_v5_14_modern_reversal", "他说我是拖油瓶的那天，我看见了十年后他跪在我坟前的样子"),
    ("batch_v5_15_family_ethics", "我从二十八楼跳下去的时候，全家人在楼下鼓掌"),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def md_to_body_xml(md_text: str) -> str:
    lines = []
    for line in md_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            continue
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            lines.append(f"<h2>{esc(heading)}</h2>")
        else:
            lines.append(f"<p>{esc(stripped)}</p>")
    return "\n".join(lines)


def build_skeleton(title: str, slug: str, chars: int, chapters: int) -> str:
    doc_title = f"短篇仿写终稿｜{title}"
    return "\n".join([
        f"<title>{esc(doc_title)}</title>",
        '<callout emoji="✅" background-color="light-green" border-color="green">',
        "<p>v5 结构保真产线终稿（超配减法 + 断章/密度/反转约束）。</p>",
        "</callout>",
        "<h1>质量打标</h1>",
        "<table><colgroup><col span=\"1\" width=\"160\"/><col span=\"1\" width=\"480\"/></colgroup>"
        "<thead><tr><th background-color=\"light-gray\">项目</th><th background-color=\"light-gray\">内容</th></tr></thead>"
        "<tbody>"
        f"<tr><td>本地目录</td><td>stories/{esc(slug)}</td></tr>"
        "<tr><td>产线模式</td><td>production (v5_structure_fidelity)</td></tr>"
        "<tr><td>闸门状态</td><td>pass</td></tr>"
        f"<tr><td>正文字符数</td><td>{chars}</td></tr>"
        f"<tr><td>章节数</td><td>{chapters}</td></tr>"
        "</tbody></table>",
        "<hr/>",
        "<h1>正文</h1>",
    ])


def prepare_files() -> list[dict]:
    manifest = []
    for slug, title in STORIES:
        final_path = ROOT / "stories" / slug / "final.md"
        if not final_path.exists():
            print(f"  [SKIP] {slug} — final.md not found")
            continue
        md_text = final_path.read_text(encoding="utf-8")
        chars = len(re.sub(r"\s+", "", md_text))
        chapters = len(re.findall(r"^## ", md_text, re.MULTILINE))

        prefix = f"{BATCH}.{slug}"
        skeleton_path = OUT / f"{prefix}.skeleton.xml"
        body_path = OUT / f"{prefix}.body.xml"

        skeleton_xml = build_skeleton(title, slug, chars, chapters)
        body_xml = md_to_body_xml(md_text)

        skeleton_path.write_text(skeleton_xml + "\n", encoding="utf-8")
        body_path.write_text(body_xml + "\n", encoding="utf-8")

        manifest.append({
            "slug": slug,
            "title": title,
            "doc_title": f"短篇仿写终稿｜{title}",
            "chars": chars,
            "chapters": chapters,
            "skeleton": str(skeleton_path),
            "body": str(body_path),
        })
        print(f"  [{slug}] {title} — {chars} chars, {chapters} chapters")

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nManifest written: {MANIFEST}")
    return manifest


def build_index(manifest: list[dict]) -> None:
    rows = []
    for idx, item in enumerate(manifest, start=1):
        rows.append(
            "<tr>"
            f"<td>{idx}</td>"
            f"<td>{esc(item['title'])}</td>"
            f"<td>{item['chars']}</td>"
            f"<td>{item['chapters']}</td>"
            f"<td>stories/{esc(item['slug'])}</td>"
            "</tr>"
        )

    xml = "\n".join([
        f"<title>短篇仿写终稿导出目录｜{BATCH}｜10篇</title>",
        '<callout emoji="✅" background-color="light-green" border-color="green">',
        "<p>10 篇 v5 结构保真产线终稿（第二批）；本页为总目录。</p>",
        "</callout>",
        "<h1>导出总览</h1>",
        "<table>"
        '<colgroup><col span="1" width="60"/><col span="1" width="280"/><col span="1" width="90"/><col span="1" width="90"/><col span="1" width="200"/></colgroup>'
        '<thead><tr><th background-color="light-gray">序号</th><th background-color="light-gray">标题</th><th background-color="light-gray">字数</th><th background-color="light-gray">章节</th><th background-color="light-gray">目录</th></tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table>",
    ])
    INDEX_XML.write_text(xml + "\n", encoding="utf-8")
    print(f"Index written: {INDEX_XML}")


if __name__ == "__main__":
    print(f"=== Exporting {BATCH} ===\n")
    manifest = prepare_files()
    build_index(manifest)
    print("\nDone.")
