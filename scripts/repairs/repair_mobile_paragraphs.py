"""F1 repairer: split offending multi-sentence paragraphs into single-sentence
paragraphs for tomato mobile readability.

Strategy:
- For non-dialogue paragraphs containing >=2 sentence-end marks (。!?；;), split
  on those marks and emit one paragraph per sentence.
- For dialogue paragraphs (containing 「」 or 『』 or "「" pattern), avoid hard
  splits which would break attribution; instead, downgrade inner ``。`` to ``,``
  to preserve a single end-mark while leaving prosody intact.
- Anything still offending after the safe pass is recorded as ``manual_review``.

The repairer rewrites ``draft.md``, ``draft-scenes/*.md``, ``final.md``,
``final-chapters/*.md`` in-place (no backup; pipeline backups already cover this
through draft-vN.md / runs/ snapshots).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

SENTENCE_END_RE = re.compile(r"[。！？!?；;]")
DIALOG_OPEN = ("「", "『")
DIALOG_CLOSE = ("」", "』")


def _is_heading(line: str) -> bool:
    return line.lstrip().startswith("#")


def _is_table(paragraph: str) -> bool:
    lines = [line for line in paragraph.splitlines() if line.strip()]
    if not lines:
        return False
    return all(line.lstrip().startswith("|") for line in lines)


def _has_dialog(paragraph: str) -> bool:
    return any(ch in paragraph for ch in DIALOG_OPEN) or any(ch in paragraph for ch in DIALOG_CLOSE)


def _split_paragraph(paragraph: str) -> Tuple[List[str], bool]:
    """Return (resulting paragraphs, whether the original needed manual review)."""
    if _is_heading(paragraph) or _is_table(paragraph):
        return [paragraph], False

    end_count = len(SENTENCE_END_RE.findall(paragraph))
    if end_count <= 1:
        return [paragraph], False

    if not _has_dialog(paragraph):
        # Hard split on sentence boundaries
        parts = re.split(r"(?<=[。！？!?；;])", paragraph)
        cleaned = [p.strip() for p in parts if p.strip()]
        return cleaned or [paragraph], False

    # Dialogue path: convert inner 。 (not the last one) to ，
    chars = list(paragraph)
    end_indexes = [i for i, ch in enumerate(chars) if ch in "。！？!?；;"]
    if len(end_indexes) <= 1:
        return [paragraph], False
    # Keep only the very last sentence-end as-is; replace earlier 。 with ，
    for i in end_indexes[:-1]:
        if chars[i] == "。":
            chars[i] = "，"
        elif chars[i] in "；;":
            chars[i] = "，"
        # 「！？」 inside dialogue often carries semantic weight; leave as-is and
        # mark for manual review below.
    rebuilt = "".join(chars)
    remaining = len(SENTENCE_END_RE.findall(rebuilt))
    needs_review = remaining > 1
    return [rebuilt], needs_review


def _process_text(text: str) -> Tuple[str, int, List[str]]:
    paragraphs = re.split(r"(\n\s*\n)", text)
    out_parts: List[str] = []
    fixed_count = 0
    manual_review: List[str] = []
    for chunk in paragraphs:
        if not chunk.strip() or chunk.strip("\n") == "":
            out_parts.append(chunk)
            continue
        new_paragraphs, needs_review = _split_paragraph(chunk.strip())
        if needs_review:
            manual_review.append(chunk.strip()[:80])
        if [chunk.strip()] != new_paragraphs:
            fixed_count += 1
            out_parts.append("\n\n".join(new_paragraphs))
        else:
            out_parts.append(chunk)
    return "".join(out_parts), fixed_count, manual_review


def _candidate_files(story: Path) -> List[Path]:
    candidates: List[Path] = []
    for rel in ("draft.md", "final.md"):
        path = story / rel
        if path.exists():
            candidates.append(path)
    for sub in ("draft-scenes", "final-chapters"):
        directory = story / sub
        if directory.is_dir():
            candidates.extend(sorted(directory.glob("*.md")))
    return candidates


def run(story: Path, mode: str = "production") -> Dict[str, Any]:
    files = _candidate_files(story)
    fixed_files: List[Dict[str, Any]] = []
    manual_review: List[Dict[str, str]] = []
    for path in files:
        original = path.read_text(encoding="utf-8")
        new_text, fixed_count, paragraphs = _process_text(original)
        if new_text != original:
            path.write_text(new_text, encoding="utf-8")
            fixed_files.append({"path": str(path.relative_to(story)), "fixed_paragraphs": fixed_count})
        for snippet in paragraphs:
            manual_review.append({"path": str(path.relative_to(story)), "snippet": snippet})
    return {
        "name": "mobile_paragraphs",
        "status": "ok" if not manual_review else "manual_review_required",
        "fixed_files": fixed_files,
        "manual_review": manual_review,
    }


if __name__ == "__main__":
    import argparse, json, sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--mode", default="production")
    args = parser.parse_args()
    result = run(Path(args.story), args.mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] in {"ok", "skipped"} else 1)
