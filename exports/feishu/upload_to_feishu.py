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
    cmd = ["lark-cli", *args]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}")
    obj = extract_json(proc.stdout)
    if not obj.get("ok"):
        raise RuntimeError(f"lark-cli returned ok=false for {' '.join(cmd)}\n{proc.stdout}")
    return obj


def content_arg(path: str) -> str:
    return "@" + str(Path(path).resolve().relative_to(ROOT))


def document_from_create(obj: dict) -> dict[str, str]:
    document = obj.get("data", {}).get("document", {})
    doc_id = document.get("document_id") or document.get("token") or ""
    url = document.get("url") or ""
    if not doc_id and not url:
        raise RuntimeError(f"Create response did not include document id/url:\n{json.dumps(obj, ensure_ascii=False, indent=2)}")
    return {"document_id": doc_id, "url": url}


def create_doc(content_path: str) -> dict[str, str]:
    created = run_lark(
        [
            "docs",
            "+create",
            "--api-version",
            "v2",
            "--parent-position",
            "my_library",
            "--content",
            content_arg(content_path),
        ]
    )
    return document_from_create(created)


def append_doc(doc: str, content_path: str) -> None:
    run_lark(
        [
            "docs",
            "+update",
            "--api-version",
            "v2",
            "--doc",
            doc,
            "--command",
            "append",
            "--content",
            content_arg(content_path),
        ]
    )


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
            "<p>10 篇短篇仿写 production 产线终稿已导出为独立飞书文档；本页为总目录。</p>",
            "</callout>",
            "<h1>导出总览</h1>",
            "<table>"
            '<colgroup><col span="1" width="60"/><col span="1" width="360"/><col span="1" width="90"/><col span="1" width="90"/><col span="1" width="120"/></colgroup>'
            '<thead><tr><th background-color="light-gray">序号</th><th background-color="light-gray">标题</th><th background-color="light-gray">字数</th><th background-color="light-gray">章节</th><th background-color="light-gray">链接</th></tr></thead>'
            f"<tbody>{''.join(rows)}</tbody></table>",
            "<hr/>",
            "<h1>本地追踪</h1>",
            "<p>导出目录：exports/feishu</p>",
            f"<p>导出时间：{esc(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</p>",
        ]
    )
    INDEX_XML.write_text(xml + "\n", encoding="utf-8")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    results: list[dict[str, object]] = []

    for idx, item in enumerate(manifest, start=1):
        print(f"[{idx}/10] create: {item['title']}", flush=True)
        doc = create_doc(item["skeleton"])
        target = doc["url"] or doc["document_id"]
        print(f"[{idx}/10] append body: {target}", flush=True)
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
    payload = {"index": index_doc, "stories": results}
    RESULTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
