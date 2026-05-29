#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exports" / "feishu"
MANIFEST = OUT / "manifest.json"
RESULTS = OUT / "feishu-docs.json"
INDEX_XML = OUT / "feishu-index.xml"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


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
        if output[idx + end :].strip():
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
        raise RuntimeError(f"lark-cli returned ok=false: lark-cli {' '.join(args)}\n{proc.stdout}")
    return obj


def content_arg(path: Path) -> str:
    return "@" + str(path.resolve().relative_to(ROOT))


def overwrite_doc(doc_url: str, content_path: Path) -> None:
    run_lark(
        [
            "docs",
            "+update",
            "--api-version",
            "v2",
            "--doc",
            doc_url,
            "--command",
            "overwrite",
            "--content",
            content_arg(content_path),
        ]
    )


def build_full_xml(item: dict[str, object]) -> Path:
    skeleton = Path(str(item["skeleton"]))
    body = Path(str(item["body"]))
    full = OUT / f"{item['slug']}.full.xml"
    full.write_text(
        skeleton.read_text(encoding="utf-8").rstrip()
        + "\n"
        + body.read_text(encoding="utf-8").rstrip()
        + "\n",
        encoding="utf-8",
    )
    return full


def build_index(results: list[dict[str, object]]) -> None:
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
    xml = "\n".join(
        [
            "<title>短篇仿写终稿导出目录｜10篇</title>",
            '<callout emoji="✅" background-color="light-green" border-color="green">',
            "<p>10 篇已更新为直接投稿版：补开篇导语、自然付费节点、一句一段移动端格式。</p>",
            "</callout>",
            "<h1>导出总览</h1>",
            "<table>"
            '<colgroup><col span="1" width="60"/><col span="1" width="360"/><col span="1" width="90"/><col span="1" width="90"/><col span="1" width="120"/></colgroup>'
            '<thead><tr><th background-color="light-gray">序号</th><th background-color="light-gray">标题</th><th background-color="light-gray">字数</th><th background-color="light-gray">章节</th><th background-color="light-gray">链接</th></tr></thead>'
            f"<tbody>{''.join(rows)}</tbody></table>",
            "<hr/>",
            "<h1>版本说明</h1>",
            "<ul><li>正文不显式标注付费点。</li><li>付费节点地图已放入各篇投稿包。</li><li>正文段落已统一为一句一段。</li></ul>",
            f"<p>更新时间：{esc(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>",
        ]
    )
    INDEX_XML.write_text(xml + "\n", encoding="utf-8")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    docs_by_slug = {item["slug"]: item for item in results["stories"]}
    refreshed = []

    for idx, item in enumerate(manifest, start=1):
        doc = docs_by_slug[item["slug"]]
        full_xml = build_full_xml(item)
        print(f"[{idx}/10] overwrite: {item['title']}", flush=True)
        overwrite_doc(doc["url"], full_xml)
        refreshed.append({**doc, "chars": item["chars"], "chapters": item["chapters"]})

    refreshed_by_slug = {item["slug"]: item for item in refreshed}
    ordered = [refreshed_by_slug[item["slug"]] for item in manifest]
    build_index(ordered)
    print("[index] overwrite directory document", flush=True)
    overwrite_doc(results["index"]["url"], INDEX_XML)

    payload = {"index": results["index"], "stories": ordered, "refreshed_at": datetime.now().isoformat(timespec="seconds")}
    RESULTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
