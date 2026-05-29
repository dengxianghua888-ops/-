#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exports" / "feishu"
BATCH = "batch_v3_20260526"
MANIFEST = OUT / f"manifest.{BATCH}.json"
RESULTS = OUT / f"feishu-docs.{BATCH}.json"
INDEX_XML = OUT / f"feishu-index.{BATCH}.xml"

STORIES = [
    ("batch_v3_01_modern_reversal", "录音笔"),
    ("batch_v3_02_family_ethics", "骨灰盒"),
    ("batch_v3_03_ancient_BE", "长明灯"),
    ("batch_v3_04_ancient_sweet", "满城笑我不读书"),
    ("batch_v3_05_apocalypse", "她们说我是废物"),
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
        "<p>v3 文风保真产线终稿。正文保留 final.md 定稿内容。</p>",
        "</callout>",
        "<h1>质量打标</h1>",
        "<table><colgroup><col span=\"1\" width=\"160\"/><col span=\"1\" width=\"480\"/></colgroup>"
        "<thead><tr><th background-color=\"light-gray\">项目</th><th background-color=\"light-gray\">内容</th></tr></thead>"
        "<tbody>"
        f"<tr><td>本地目录</td><td>stories/{esc(slug)}</td></tr>"
        "<tr><td>产线模式</td><td>production (v3_style_fidelity)</td></tr>"
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

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest written: {MANIFEST}")
    print(f"Prepared {len(manifest)} stories for upload.")
    return manifest


def extract_json(output: str) -> dict:
    output = output.strip()
    decoder = json.JSONDecoder()
    for idx, ch in enumerate(output):
        if ch != "{":
            continue
        try:
            obj, end = decoder.raw_decode(output[idx:])
        except json.JSONDecodeError:
            continue
        if output[idx + end:].strip():
            continue
        return obj
    raise ValueError(f"Could not parse JSON from lark-cli output:\n{output}")


def run_lark(args: list[str]) -> dict:
    proc = subprocess.run(
        ["lark-cli", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): lark-cli {' '.join(args)}\n{proc.stdout}")
    obj = extract_json(proc.stdout)
    if not obj.get("ok"):
        raise RuntimeError(f"lark-cli returned ok=false for lark-cli {' '.join(args)}\n{proc.stdout}")
    return obj


def content_arg(path: str) -> str:
    return "@" + str(Path(path).resolve().relative_to(ROOT))


def create_doc(content_path: str) -> dict[str, str]:
    created = run_lark([
        "docs", "+create",
        "--api-version", "v2",
        "--as", "user",
        "--parent-position", "my_library",
        "--content", content_arg(content_path),
    ])
    document = created.get("data", {}).get("document", {})
    doc_id = document.get("document_id") or document.get("token") or ""
    url = document.get("url") or ""
    if not doc_id and not url:
        raise RuntimeError(f"Create response did not include document id/url:\n{json.dumps(created, ensure_ascii=False, indent=2)}")
    return {"document_id": doc_id, "url": url}


def append_doc(doc: str, content_path: str) -> None:
    run_lark([
        "docs", "+update",
        "--api-version", "v2",
        "--as", "user",
        "--doc", doc,
        "--command", "append",
        "--content", content_arg(content_path),
    ])


def build_index(results: list[dict]) -> None:
    rows = []
    for item in results:
        rows.append(
            "<tr>"
            f"<td>{esc(item['idx'])}</td>"
            f"<td>{esc(item['title'])}</td>"
            f"<td>{esc(item['chars'])}</td>"
            f"<td>{esc(item['chapters'])}</td>"
            f"<td><a href=\"{esc(item['url'])}\">打开文档</a></td>"
            "</tr>"
        )

    xml = "\n".join([
        f"<title>短篇仿写终稿导出目录｜{BATCH}｜5篇</title>",
        '<callout emoji="✅" background-color="light-green" border-color="green">',
        "<p>5 篇 v3 文风保真产线终稿已导出为独立飞书文档；本页为总目录。</p>",
        "</callout>",
        "<h1>导出总览</h1>",
        "<table>"
        '<colgroup><col span="1" width="60"/><col span="1" width="200"/><col span="1" width="90"/><col span="1" width="90"/><col span="1" width="120"/></colgroup>'
        '<thead><tr><th background-color="light-gray">序号</th><th background-color="light-gray">标题</th><th background-color="light-gray">字数</th><th background-color="light-gray">章节</th><th background-color="light-gray">链接</th></tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table>",
        "<hr/>",
        "<h1>版本说明</h1>",
        "<ul><li>v3_style_fidelity 产线，rhythm_fit 全 PASS</li>"
        "<li>5 genres: modern_reversal / family_ethics / ancient_BE / ancient_sweet / apocalypse_heroine</li>"
        "<li>正文段落统一为一句一段</li></ul>",
        f"<p>导出时间：{esc(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>",
    ])
    INDEX_XML.write_text(xml + "\n", encoding="utf-8")


def upload(manifest: list[dict]) -> int:
    results: list[dict] = []

    for idx, item in enumerate(manifest, start=1):
        print(f"[{idx}/{len(manifest)}] create: {item['title']}", flush=True)
        doc = create_doc(item["skeleton"])
        target = doc["url"] or doc["document_id"]
        print(f"[{idx}/{len(manifest)}] append body: {target}", flush=True)
        append_doc(target, item["body"])
        result = {
            "idx": idx,
            "slug": item["slug"],
            "title": item["title"],
            "doc_title": item["doc_title"],
            "chars": item["chars"],
            "chapters": item["chapters"],
            **doc,
        }
        results.append(result)
        RESULTS.write_text(json.dumps({"stories": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    build_index(results)
    print("[index] create directory document", flush=True)
    index_doc = create_doc(str(INDEX_XML))
    payload = {
        "index": index_doc,
        "stories": results,
        "exported_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "result_file": str(RESULTS),
    }
    RESULTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)
    return 0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    manifest = prepare_files()
    if mode == "prepare":
        print("Prepare-only mode: files written, no upload.")
        return 0
    return upload(manifest)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
