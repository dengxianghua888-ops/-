"""Emit a phase-5 rewrite todo when draft rhythm drifts from the source."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from rhythm_metrics import rhythm_fit


def _instructions(failures: List[str]) -> List[str]:
    notes = [
        "保持每个 scene 的事件和字数区间不变,只修节奏。",
        "保留直接对白、弹幕、章尾钩和现有信息增量,不要删成概要。",
        "不得新增旁白解释、环境铺陈、流程清单或重复情绪总结。",
    ]
    joined = "\n".join(failures)
    if "below source-rhythm floor" in joined or "over-fragments" in joined:
        notes.extend(
            [
                "把被拆成两行的半句合并成完整短句,例如原因+结果、动作+反应、台词提示+动作可放回同一行。",
                "目标是接近源文平均可视行长,不是把短行率推到 100%。",
                "每行必须是一句完整、有信息量的短句;不要写成诗行。",
            ]
        )
    if "exceeds source-fast ceiling" in joined or "below source-fit floor" in joined:
        notes.extend(
            [
                "删掉无新信息长句,把流程说明改成短对白、现场动作或证据翻转。",
                "若需要补字数,补短对白/动作/证据变化,不要补解释。",
            ]
        )
    if "quote_line_rate" in joined:
        if "over-cranks" in joined:
            notes.append("减少连续对白逼问,把部分角色追问改成女主慢半拍反应、生活动作或弹幕吐槽。")
        else:
            notes.append("恢复中文引号里的直接对白,不要用他说/她说转述替代。")
    if "barrage_line_rate" in joined:
        notes.append("恢复弹幕/评论的节奏功能,每章保留吐槽、误导、卡顿或剧透碎片;不要让对白替代弹幕。")
    if "question_marks_per_k" in joined:
        if "over-cranks" in joined:
            notes.append("降低问号密度,删掉连续逼问;优先改成陈述式动作、弹幕感叹、迟钝确认或生活照顾。")
        else:
            notes.append("恢复原文式反问和弹幕疑问,但每个问题必须推动信息差。")
    return notes


def run(story: Path, mode: str = "production") -> Dict[str, Any]:
    source_path = story / "source.md"
    draft_path = story / "draft.md"
    if not source_path.exists() or not draft_path.exists():
        return {"name": "source_rhythm", "status": "skipped", "reason": "source.md or draft.md missing"}

    result = rhythm_fit(
        source_path.read_text(encoding="utf-8"),
        draft_path.read_text(encoding="utf-8"),
    )
    todo_path = story / "source-rhythm-rewrite-todo.json"
    payload = {
        "status": result["status"],
        "applicable": result.get("applicable", False),
        "source": result.get("source", {}),
        "candidate": result.get("candidate", {}),
        "failures": result.get("failures", []),
        "rewrite_instructions": _instructions(list(result.get("failures", []))),
    }
    todo_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if result["status"] == "pass":
        return {"name": "source_rhythm", "status": "ok", "todo_path": str(todo_path.relative_to(story))}
    return {
        "name": "source_rhythm",
        "status": "manual_review_required",
        "failures": result.get("failures", []),
        "todo_path": str(todo_path.relative_to(story)),
    }
