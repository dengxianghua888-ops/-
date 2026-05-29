#!/usr/bin/env python3
"""Deterministically package production draft scenes into submission artifacts.

This is intentionally boring: phase 5 already owns prose generation. The
packager keeps the vetted scene order, adds a short guide, writes chapter files,
and creates the Tomato submission/paywall map expected by phase 7 validators.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml


def count_nonspace(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_paragraphs(text: str) -> List[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def split_sentences(paragraph: str) -> List[str]:
    paragraph = re.sub(r"\s+", "", paragraph.strip())
    if not paragraph:
        return []
    if paragraph.startswith("#"):
        return [paragraph]
    if paragraph.startswith("【") and paragraph.endswith("】"):
        return [paragraph]
    if re.fullmatch(r"[“\"「『].+[”\"」』]", paragraph):
        return [paragraph]

    out: List[str] = []
    start = 0
    index = 0
    while index < len(paragraph):
        if paragraph[index] in "。！？!?；;":
            end = index + 1
            while end < len(paragraph) and paragraph[end] in "”’』」）》）】\"'":
                end += 1
            sentence = paragraph[start:end].strip()
            if sentence:
                out.append(sentence)
            start = end
            index = end
            continue
        index += 1
    tail = paragraph[start:].strip()
    if tail:
        out.append(tail)
    return out or [paragraph]


QUESTION_HINT_RE = re.compile(r"(为什么|为何|谁|哪里|怎么|能否|是否|究竟|到底|会不会|有没有|是什么|哪)")
TERMINAL_PUNCT_RE = re.compile(r"[。！？!?](?:[”\"」』】）)\]'》]*)$")
MID_SENTENCE_PUNCT_RE = re.compile(r"[，、：；,;](?:[”\"」』】）)\]'》]*)$")
QUOTE_START = ("“", "\"", "「", "『")
SCENE_META_LINE_RE = re.compile(
    r"(事实层面|价值层面|程序层面|关系层面|情绪层面|社会性新生|轮回终止|"
    r"主角获得|主线爽感|尊重型修复|价值反转|情绪债|人物弧|读者|"
    r"付费点|付费卡点|卡点|伏笔|铺垫|爽感|终局黑切|补叙|旧关系交代|"
    r"最后留下的是判词|公开承认能否|不抢主线|给出.*修复|把爱情.*判成|"
    r"寒心感|砸实|别给缓冲|连续发生|补救空间|落地到|行业切割|"
    r"还有没有机会|有没有任何|知道数字没有|知道多少.*真相|"
    r"具体写了什么|被剪掉的部分是什么|发生过什么|到底遭遇过什么|"
    r"真不知道还是不肯知道)",
    re.I,
)
INFO_GAP_META_RE = re.compile(
    r"；.*(?:什么|为什么|谁|是否|是不是|有没有|还有没有|能否|能不能|到底|几天|知道多少|知道.*没有|真不知道|不肯知道|补救)",
    re.I,
)
QUESTION_WORD_META_RE = re.compile(r"^(?!.*[“\"「『]).*(?:为什么|为何|什么|谁|是否|是不是|有没有|还有没有|能否|能不能|到底|几天|怎么).*$")


def is_scene_meta_line(line: str) -> bool:
    compact = re.sub(r"\s+", "", line.strip())
    if not compact:
        return False
    if compact.startswith(QUOTE_START):
        return False
    has_quote = any(mark in compact for mark in QUOTE_START)
    if has_quote and not SCENE_META_LINE_RE.search(compact):
        return False
    return bool(
        SCENE_META_LINE_RE.search(compact)
        or INFO_GAP_META_RE.search(compact)
        or QUESTION_WORD_META_RE.search(compact)
    )


def collect_card_meta_values(value: Any, key: str = "") -> List[str]:
    if isinstance(value, dict):
        out: List[str] = []
        for child_key, child_value in value.items():
            out.extend(collect_card_meta_values(child_value, str(child_key)))
        return out
    if isinstance(value, list):
        out = []
        for child in value:
            out.extend(collect_card_meta_values(child, key))
        return out
    text = str(value or "").strip()
    return [text] if count_nonspace(text) >= 6 else []


def card_meta_norms(card: Dict[str, Any]) -> set[str]:
    return {normalized_for_dedupe(value) for value in collect_card_meta_values(card) if normalized_for_dedupe(value)}


def normalized_for_dedupe(text: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", text)


def dedupe_tail_paragraphs(paragraphs: List[str]) -> List[str]:
    out = paragraphs[:]
    while len(out) > 1:
        last = out[-1]
        previous = normalized_for_dedupe("".join(out[-14:-1]))
        cores = [last]
        if "：" in last or ":" in last:
            cores.append(re.split(r"[:：]", last, maxsplit=1)[-1])
        quoted = re.findall(r"[“\"「『]([^”\"」』]{6,})[”\"」』]?", last)
        cores.extend(quoted)
        duplicate = False
        for core_index, core in enumerate(cores):
            core_norm = normalized_for_dedupe(core)
            min_len = 5 if core_index > 0 else 10
            if core_norm and len(core_norm) >= min_len and core_norm in previous:
                duplicate = True
                break
        if duplicate:
            out.pop()
            continue
        break
    return out


def paragraph_quote_rate(paragraphs: List[str]) -> float:
    if not paragraphs:
        return 0.0
    return sum(1 for paragraph in paragraphs if paragraph.strip().startswith(QUOTE_START)) / len(paragraphs)


def reduce_quote_pressure(paragraphs: List[str], max_quote_rate: float | None) -> List[str]:
    return paragraphs


def smooth_short_narration(paragraphs: List[str]) -> List[str]:
    """Join tiny adjacent narration beats while preserving one sentence per line."""
    out: List[str] = []
    index = 0
    blocked_starts = ("#", "【", "“", "\"", "「", "『")
    while index < len(paragraphs):
        current = paragraphs[index].strip()
        if (
            index + 1 < len(paragraphs)
            and current
            and not current.startswith(blocked_starts)
            and count_nonspace(current) <= 16
        ):
            nxt = paragraphs[index + 1].strip()
            if (
                nxt
                and not nxt.startswith(blocked_starts)
                and count_nonspace(nxt) <= 22
            ):
                merged = re.sub(r"[。！？!?；;]+$", "，", current) + nxt
                out.append(ensure_terminal_punctuation(merged))
                index += 2
                continue
        out.append(current)
        index += 1
    return out


def ensure_terminal_punctuation(paragraph: str) -> str:
    if paragraph.startswith("#") or TERMINAL_PUNCT_RE.search(paragraph):
        return paragraph
    return paragraph + ("？" if QUESTION_HINT_RE.search(paragraph) else "。")


def mobile_paragraphs(
    text: str,
    extra_meta_norms: set[str] | None = None,
    max_quote_rate: float | None = None,
) -> List[str]:
    out: List[str] = []
    pending = ""
    meta_norms = extra_meta_norms or set()
    for paragraph in split_paragraphs(text):
        compact = re.sub(r"\s+", "", paragraph.strip())
        if not compact:
            continue
        compact_norm = normalized_for_dedupe(compact)
        if is_scene_meta_line(compact) or (not any(mark in compact for mark in QUOTE_START) and compact_norm in meta_norms):
            continue
        current = pending + compact if pending else compact
        if MID_SENTENCE_PUNCT_RE.search(current):
            pending = current
            continue
        out.extend(ensure_terminal_punctuation(sentence) for sentence in split_sentences(current))
        pending = ""
    if pending:
        out.extend(
            ensure_terminal_punctuation(sentence)
            for sentence in split_sentences(pending.rstrip("，、：；,;"))
        )
    out = dedupe_tail_paragraphs(out)
    out = smooth_short_narration(out)
    return reduce_quote_pressure(out, max_quote_rate)


def source_quote_limit(story: Path) -> float | None:
    source_path = story / "source.md"
    if not source_path.exists():
        return None
    lines = [
        line.strip()
        for line in source_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines:
        return None
    source_rate = sum(1 for line in lines if any(mark in line for mark in QUOTE_START)) / len(lines)
    return min(0.62, source_rate + 0.16)


def scene_number(path: Path) -> int:
    match = re.search(r"scene-(\d+)", path.stem)
    if not match:
        return 0
    return int(match.group(1))


def chapter_hook(text: str, fallback: str) -> str:
    for line in reversed(text.splitlines()):
        stripped = line.strip().strip("#").strip()
        if stripped and count_nonspace(stripped) >= 8:
            return stripped[:80]
    return fallback


HOOK_META_RE = re.compile(
    r"(截断句|章尾钩子|chapter_end_hook|hook|终局价值|留到终局|draft-scenes|/Users/|```|FILE:|END FILE)",
    re.I,
)
HOOK_PREFIX_RE = re.compile(r"^(?:截断句|章尾钩子|本章悬念|hook|chapter_end_hook)\s*[:：]\s*", re.I)


def normalize_hook(raw: str, fallback: str) -> str:
    text = str(raw or "").strip()
    text = re.sub(r"^`{3,}\w*", "", text).strip()
    text = re.sub(r"`{3,}$", "", text).strip()
    text = re.sub(r"\([^)]*(?:/Users/|draft-scenes|FILE:|END FILE)[^)]*\)", "", text).strip()
    text = HOOK_PREFIX_RE.sub("", text).strip()

    candidates = [line.strip(" -\t") for line in text.splitlines() if line.strip()]
    for candidate in candidates or [text]:
        candidate = HOOK_PREFIX_RE.sub("", candidate).strip()
        if count_nonspace(candidate) >= 8 and not HOOK_META_RE.search(candidate):
            return candidate[:80]
    return fallback


def selected_candidate(data: Dict[str, Any]) -> Dict[str, Any]:
    selected = data.get("selected_candidate")
    candidates = data.get("candidates") or []
    if isinstance(selected, dict):
        return selected
    for item in candidates:
        if isinstance(item, dict) and str(item.get("id")) == str(selected):
            return item
    return candidates[0] if candidates and isinstance(candidates[0], dict) else {}


def build_lead(story: Path, bible: Dict[str, Any]) -> List[str]:
    brief = load_json(story / "story-brief.json") if (story / "story-brief.json").exists() else {}
    room = load_json(story / "adaptation-room.json") if (story / "adaptation-room.json").exists() else {}
    candidate = selected_candidate(room)
    chapters = bible.get("chapters") or []
    first_hook = normalize_hook(str((chapters[0] or {}).get("chapter_end_hook") or ""), "") if chapters else ""
    mid_hook = normalize_hook(str((chapters[min(len(chapters) // 2, len(chapters) - 1)] or {}).get("chapter_end_hook") or ""), "") if chapters else ""
    final_hook = normalize_hook(str((chapters[-1] or {}).get("chapter_end_hook") or ""), "") if chapters else ""
    reader_promise = str(brief.get("reader_promise") or candidate.get("premise") or "").strip()

    line1 = f"导语：{first_hook}" if first_hook else f"导语：{bible.get('title', story.name)}开局就把误会、证据和身份反转推到我面前。"
    line2 = mid_hook or reader_promise[:70] or "所有人都以为这是普通的情感拉扯，只有我一路把证据攥在手里。"
    line3 = final_hook or "等最后一层真相落地，先前所有轻慢，都成了反击的证据。"

    cleaned = []
    for line in [line1, line2, line3]:
        compact = re.sub(r"\s+", "", line).strip()
        cleaned.append(ensure_terminal_punctuation(compact))
    return cleaned


def write_story_yaml(story: Path, title: str, chapter_count: int) -> None:
    path = story / "story.yaml"
    data: Dict[str, Any] = {}
    if path.exists():
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            data = {}
    data["slug"] = data.get("slug") or story.name
    data["status"] = "final"
    data["pipeline_mode"] = "production"
    data.setdefault("final_packaging", {})
    data["final_packaging"].update(
        {
            "title": title,
            "final_file": "final.md",
            "craft_notes_file": "craft-notes.md",
            "submission_file": "tomato-submission.md",
            "chapters_map": "final-chapters/_chapters-map.md",
            "chapter_count": chapter_count,
            "chapter_files": [f"final-chapters/ch{index:02d}.md" for index in range(1, chapter_count + 1)],
            "packager": "scripts/package_from_draft_scenes.py",
        }
    )
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    args = parser.parse_args()

    story = Path(args.story)
    bible = load_json(story / "beat-bible.json")
    title = str(bible.get("title") or story.name)
    scene_paths = sorted((story / "draft-scenes").glob("scene-*.md"), key=scene_number)
    card_paths = sorted((story / "scene-cards").glob("scene-*.json"), key=scene_number)
    cards = [load_json(path) for path in card_paths]
    card_by_scene = {str(card.get("scene_id")): card for card in cards}
    if not scene_paths:
        raise SystemExit("missing draft-scenes/scene-*.md")
    draft_text = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in scene_paths if path.read_text(encoding="utf-8").strip()).strip()
    if draft_text:
        (story / "draft.md").write_text(draft_text + "\n", encoding="utf-8")

    chapters_dir = story / "final-chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    for old in chapters_dir.glob("ch*.md"):
        old.unlink()

    lead = build_lead(story, bible)
    final_parts: List[str] = [f"# {title}", *lead]
    map_lines = ["| 章 | 字数 | 本章悬念 |", "|---|---:|---|"]
    paywall_rows: List[tuple[int, str]] = []
    chapters_meta: List[Dict[str, Any]] = []
    quote_limit = source_quote_limit(story)

    for index, scene_path in enumerate(scene_paths, start=1):
        scene_id = scene_path.stem
        card = card_by_scene.get(scene_id, {})
        chapter_title = str(card.get("chapter_title") or card.get("title") or f"第{index}章")
        if not chapter_title.startswith("第"):
            chapter_title = f"第{index}章"
        body = "\n\n".join(
            mobile_paragraphs(scene_path.read_text(encoding="utf-8"), card_meta_norms(card), quote_limit)
        )
        hook = normalize_hook(str(card.get("chapter_end_hook") or ""), chapter_hook(body, f"第{index}章悬念继续升级"))
        chapter_text = f"# {chapter_title}\n\n{body.strip()}\n"
        chapter_file = chapters_dir / f"ch{index:02d}.md"
        chapter_file.write_text(chapter_text, encoding="utf-8")
        chars = count_nonspace(body)
        chapters_meta.append({"chapter": index, "chars": chars, "hook": hook})
        final_parts.append(f"## {chapter_title}")
        final_parts.append(body.strip())
        map_lines.append(f"| {index:02d} | {chars} | {hook} |")
        if card.get("paywall_card"):
            paywall_rows.append((index, hook))

    final_text = "\n\n".join(part.strip() for part in final_parts if part.strip()) + "\n"
    (story / "final.md").write_text(final_text, encoding="utf-8")
    (chapters_dir / "_chapters-map.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8")

    required_paywalls = max(1, math.ceil(max(count_nonspace(final_text), 10000) / 3500))
    if len(paywall_rows) < required_paywalls:
        used = {row[0] for row in paywall_rows}
        for meta in chapters_meta:
            if len(paywall_rows) >= required_paywalls:
                break
            if meta["chapter"] not in used:
                paywall_rows.append((int(meta["chapter"]), str(meta["hook"])))

    submission = [
        f"# {title}",
        "",
        "## 简介",
        "",
        *lead,
        "",
        "## 付费节点地图（直接投稿版）",
        "",
        "正文不显式标注付费点，节点已自然落在章末或强悬念句上。",
        "",
        "| 节点 | 位置 | 自然卡点 |",
        "|---|---|---|",
    ]
    for row_index, (chapter_no, hook) in enumerate(paywall_rows, start=1):
        submission.append(f"| {row_index} | 第 {chapter_no} 章末 | {hook} |")
    (story / "tomato-submission.md").write_text("\n".join(submission).rstrip() + "\n", encoding="utf-8")

    craft = [
        "# Craft Notes",
        "",
        "- Phase 5 split-scene output was packaged deterministically.",
        "- final.md keeps the generated scene order and adds a three-paragraph opening guide.",
        "- final-chapters mirror draft-scenes one-to-one for stable chapter length and hook coverage.",
        "- tomato-submission.md includes a direct-submission paywall map without visible labels in body text.",
    ]
    (story / "craft-notes.md").write_text("\n".join(craft) + "\n", encoding="utf-8")
    write_story_yaml(story, title, len(scene_paths))
    print(json.dumps({"story": str(story), "title": title, "chapters": len(scene_paths), "chars": count_nonspace(final_text)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
