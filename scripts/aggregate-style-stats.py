#!/usr/bin/env python3
"""
aggregate-style-stats.py -- 扫描 corpus/{slug}/analysis/style-dna.md 和
stories/*/analysis/style-dna.md,提取定量字段,按 genre 聚合 mean/std,
写入 context/style-dna-stats.json。

后续 dissector Step 3(Style DNA)可加载该 JSON 作为先验均值,指导新
案例的文风定量分析。

抽取的字段:
  - avg_sentence_length        平均句长(字)
  - dialogue_ratio             对话占比(0-1)
  - rhetorical_question_per_k  反问-自答句密度(每千字次数)
  - physical_emotion_per_k     物理化金句密度(每千字次数)
  - couplet_per_k              对仗反讽句密度(每千字次数)

字段名称不强制,脚本做宽松匹配(如支持"平均句长"/"avg_sentence_length"/"avg sentence length")。

用法:
  python3 scripts/aggregate-style-stats.py
  python3 scripts/aggregate-style-stats.py --corpus /path/to/corpus --stats /path/to/stats.json
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


# --------- 通用抽取器 ---------

def _to_float(s: str) -> Optional[float]:
    """把 '18 字' '35%' '3.2/千字' 之类抽出为 float"""
    if not s:
        return None
    # 去百分号,转为 0-1
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", s)
    if m:
        return float(m.group(1)) / 100.0
    # 直接的数字
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    if m:
        return float(m.group(1))
    return None


def _extract_range_mid(s: str) -> Optional[float]:
    """15-20 字 → 17.5"""
    m = re.search(r"(\d+(?:\.\d+)?)\s*[-~至到]\s*(\d+(?:\.\d+)?)", s)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0
    return _to_float(s)


def parse_style_dna(text: str) -> Dict[str, Optional[float]]:
    """尽力抽取 style-dna.md 的定量字段。未命中返回 None。"""
    out = {
        "avg_sentence_length": None,
        "dialogue_ratio": None,
        "rhetorical_question_per_k": None,
        "physical_emotion_per_k": None,
        "couplet_per_k": None,
    }

    # 平均句长: "平均句长: 18 字" / "- 平均句长: X 字"
    m = re.search(r"平均句长[：: ]*([^\n]+)", text)
    if m:
        out["avg_sentence_length"] = _extract_range_mid(m.group(1))

    # 对话占比: "对话占比: 40%" / "对话占比: X%"
    m = re.search(r"对话占比[：: ]*([^\n]+)", text)
    if m:
        value = _extract_range_mid(m.group(1))
        if value is not None and value > 1:
            value = value / 100.0
        out["dialogue_ratio"] = value

    # 金句密度三类,优先匹配"X/千字"格式
    for key, patterns in [
        ("rhetorical_question_per_k", [r"反问[^0-9\n]*?(\d+(?:\.\d+)?)\s*[/每]?\s*千字"]),
        ("couplet_per_k", [r"对仗[^0-9\n]*?(\d+(?:\.\d+)?)\s*[/每]?\s*千字"]),
        ("physical_emotion_per_k", [r"物理化[^0-9\n]*?(\d+(?:\.\d+)?)\s*[/每]?\s*千字"]),
    ]:
        for p in patterns:
            m = re.search(p, text)
            if m:
                out[key] = float(m.group(1))
                break

    # beat-sheet 顶部的"金句密度"合并行:
    # 例: "金句密度: 反问-自答 3.2/千字; 对仗反讽 1.8/千字; 物理化 6.5/千字"
    m = re.search(r"金句密度[：: ]*([^\n]+)", text)
    if m:
        line = m.group(1)
        mm = re.search(r"反问[^0-9]*(\d+(?:\.\d+)?)", line)
        if mm and out["rhetorical_question_per_k"] is None:
            out["rhetorical_question_per_k"] = float(mm.group(1))
        mm = re.search(r"对仗[^0-9]*(\d+(?:\.\d+)?)", line)
        if mm and out["couplet_per_k"] is None:
            out["couplet_per_k"] = float(mm.group(1))
        mm = re.search(r"物理化[^0-9]*(\d+(?:\.\d+)?)", line)
        if mm and out["physical_emotion_per_k"] is None:
            out["physical_emotion_per_k"] = float(mm.group(1))

    return out


def read_genre(dissection_path: Path) -> Optional[str]:
    """从 dissection.md 的 yaml 头抽 genre"""
    if not dissection_path.exists():
        return None
    text = dissection_path.read_text(encoding="utf-8")
    m = re.search(r"^genre:\s*([A-Za-z_]+)", text, re.MULTILINE)
    return m.group(1) if m else None


# --------- 聚合 ---------

def _stats(values: List[float]) -> Dict[str, Optional[float]]:
    values = [v for v in values if v is not None]
    n = len(values)
    if n == 0:
        return {"mean": None, "std": None, "n": 0, "samples": []}
    mean = sum(values) / n
    if n > 1:
        var = sum((v - mean) ** 2 for v in values) / (n - 1)
        std = math.sqrt(var)
    else:
        std = 0.0
    return {"mean": round(mean, 3), "std": round(std, 3), "n": n, "samples": values}


def aggregate(corpus_dir: Path, stories_dir: Path) -> Dict:
    by_genre: Dict[str, Dict[str, List[float]]] = {}

    # 扫描 corpus/
    for slug_dir in sorted(corpus_dir.iterdir()):
        if not slug_dir.is_dir() or slug_dir.name.startswith("_"):
            continue
        dissection = slug_dir / "dissection.md"
        style_dna = slug_dir / "analysis" / "style-dna.md"
        genre = read_genre(dissection)
        if not genre:
            continue
        # 优先用 analysis/style-dna.md,次用 dissection.md 里的金句密度块
        src = style_dna.read_text(encoding="utf-8") if style_dna.exists() else dissection.read_text(encoding="utf-8")
        metrics = parse_style_dna(src)
        g = by_genre.setdefault(genre, {})
        for k, v in metrics.items():
            g.setdefault(k, []).append(v)

    # 扫描 stories/
    if stories_dir.exists():
        for slug_dir in sorted(stories_dir.iterdir()):
            if not slug_dir.is_dir():
                continue
            dissection = slug_dir / "dissection.md"
            style_dna = slug_dir / "analysis" / "style-dna.md"
            genre = read_genre(dissection)
            if not genre:
                continue
            src = style_dna.read_text(encoding="utf-8") if style_dna.exists() else (
                dissection.read_text(encoding="utf-8") if dissection.exists() else ""
            )
            if not src:
                continue
            metrics = parse_style_dna(src)
            g = by_genre.setdefault(genre, {})
            for k, v in metrics.items():
                g.setdefault(k, []).append(v)

    # 折算 mean/std
    result = {}
    for genre, fields in by_genre.items():
        result[genre] = {k: _stats(v) for k, v in fields.items()}
    return result


def main():
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent.parent
    ap.add_argument("--corpus", default=str(root / "corpus"))
    ap.add_argument("--stories", default=str(root / "stories"))
    ap.add_argument("--stats", default=str(root / "context" / "style-dna-stats.json"))
    args = ap.parse_args()

    corpus_dir = Path(args.corpus)
    stories_dir = Path(args.stories)
    stats_path = Path(args.stats)

    if not corpus_dir.is_dir():
        print(f"错误: corpus 目录不存在: {corpus_dir}", file=sys.stderr)
        sys.exit(1)

    by_genre = aggregate(corpus_dir, stories_dir)

    doc = {
        "_meta": {
            "version": 2,
            "description": "跨案例 Style DNA 定量字段聚合。",
            "source": "corpus/ + stories/ 下各 analysis/style-dna.md 与 dissection.md",
            "updated_by": "scripts/aggregate-style-stats.py",
        },
        "by_genre": by_genre,
    }

    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_path.open("w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    print(f"已写入: {stats_path}")
    for g in sorted(by_genre.keys()):
        fields = by_genre[g]
        summary = ", ".join(
            f"{k}(n={v['n']})" for k, v in fields.items() if v["n"] > 0
        ) or "(无数据)"
        print(f"  {g}: {summary}")


if __name__ == "__main__":
    main()
