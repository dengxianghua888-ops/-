#!/usr/bin/env python3
"""Prepare human calibration checklists for V4 corpus genes."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List


GENE_FIELDS = (
    "reader_promise",
    "emotional_debt_type",
    "dominant_s爽点",
    "antagonist_violation",
    "protagonist_stance",
    "payoff_pattern",
    "tomato_fit_score",
)


def has_v4_genes(entry: Dict[str, Any]) -> bool:
    return all(key in entry for key in GENE_FIELDS)


def load_index(corpus: Path) -> Dict[str, Any]:
    index_path = corpus / "_index.json"
    if not index_path.exists():
        raise ValueError(f"missing corpus index: {index_path}")
    return json.loads(index_path.read_text(encoding="utf-8"))


def score(entry: Dict[str, Any]) -> tuple:
    return (-float(entry.get("tomato_fit_score", 0) or 0), entry.get("slug", ""))


def select_candidates(entries: Iterable[Dict[str, Any]], per_genre: int) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        if entry.get("status") != "dissected":
            continue
        if not has_v4_genes(entry):
            continue
        if entry.get("v4_calibration_status") == "human_calibrated":
            continue
        groups[entry.get("genre", "(missing)")].append(entry)

    selected: List[Dict[str, Any]] = []
    for genre in sorted(groups):
        selected.extend(sorted(groups[genre], key=score)[:per_genre])
    return selected


def render_checklist(entry: Dict[str, Any]) -> str:
    mechanisms = ", ".join(entry.get("reversal_mechanisms", [])) or "待补"
    return f"""# V4 人工校准清单

```yaml
slug: {entry.get('slug', '')}
genre: {entry.get('genre', '')}
v4_calibration_status: pending_human_review
previous_status: {entry.get('v4_calibration_status', '')}
reviewer: ""
reviewed_at: ""
decision: pending # pending|approved|revise
```

## 案例信息

- **filename**: {entry.get('filename', '')}
- **word_count**: {entry.get('word_count', '')}
- **mechanisms**: [{mechanisms}]
- **dominant_s爽点(machine)**: {entry.get('dominant_s爽点', '')}
- **tomato_fit_score(machine)**: {entry.get('tomato_fit_score', '')}

## 机器基因草稿

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | {entry.get('reader_promise', '')} | |
| emotional_debt_type | {entry.get('emotional_debt_type', '')} | |
| dominant_s爽点 | {entry.get('dominant_s爽点', '')} | |
| antagonist_violation | {entry.get('antagonist_violation', '')} | |
| protagonist_stance | {entry.get('protagonist_stance', '')} | |
| payoff_pattern | {entry.get('payoff_pattern', '')} | |
| tomato_fit_score | {entry.get('tomato_fit_score', '')} | |

## 人工校准 Checklist

- [ ] 读完 `dissection.md`,确认机器 reader_promise 是否真的对应原 case 的读者承诺。
- [ ] 对照 `analysis/soul-contract.md`,确认情绪债不是泛化模板,而是该 case 特有的债。
- [ ] 对照 M1-M8,确认 dominant_s爽点 是主导爽点而非列表第一个机制。
- [ ] 检查 antagonist_violation 是否具体到“违反了什么读者道德底线”。
- [ ] 检查 protagonist_stance 是否能指导改编写手复刻主角姿态。
- [ ] 检查 payoff_pattern 是否描述了清算动作,而不是泛泛说“反派被惩罚”。
- [ ] 检查 tomato_fit_score 是否与标题点击欲、首章留存、卡点密度相符。
- [ ] 写下至少 2 条“神髓禁改项”和 2 条“可替换项”。

## 校准结论

### 调整后的爆款基因

reader_promise:

emotional_debt_type:

dominant_s爽点:

antagonist_violation:

protagonist_stance:

payoff_pattern:

tomato_fit_score:

### 神髓禁改项

1.
2.

### 可替换项

1.
2.

### 校准备注

"""


def render_plan(selected: List[Dict[str, Any]], per_genre: int) -> str:
    lines = [
        "# V4 人工校准计划",
        "",
        f"- **generated_at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **target_per_genre**: {per_genre}",
        "- **status**: pending_human_review",
        "",
        "## 校准候选",
        "",
        "| genre | slug | score | mechanisms | checklist |",
        "|-------|------|-------|------------|-----------|",
    ]
    for entry in selected:
        slug = entry.get("slug", "")
        mechanisms = ", ".join(entry.get("reversal_mechanisms", []))
        lines.append(
            f"| {entry.get('genre', '')} | {slug} | {entry.get('tomato_fit_score', '')} | "
            f"{mechanisms} | corpus/{slug}/analysis/human-calibration.md |"
        )
    lines.extend([
        "",
        "## 使用方式",
        "",
        "1. 人工阅读对应 `dissection.md` 与 V4 四件套。",
        "2. 填写每个 `human-calibration.md` 的人工校准列、禁改项、可替换项和备注。",
        "3. 只有当 `decision: approved` 且 reviewer/reviewed_at 已填写时,才允许升级为 `human_calibrated`。",
        "",
        "注意: 本计划只创建校准工作台,不会自动把 machine_draft 标记为 human_calibrated。",
    ])
    return "\n".join(lines) + "\n"


def write_text(path: Path, text: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default=str(Path(__file__).resolve().parent.parent / "corpus"))
    parser.add_argument("--per-genre", type=int, default=2)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    corpus = Path(args.corpus)
    try:
        index = load_index(corpus)
    except (ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    selected = select_candidates(index.get("entries", []), args.per_genre)
    if not selected:
        print("no machine_draft candidates found", file=sys.stderr)
        return 1

    plan_path = corpus / "_human-calibration-plan.md"
    write_text(plan_path, render_plan(selected, args.per_genre), overwrite=True)

    written = 0
    for entry in selected:
        checklist_path = corpus / entry["slug"] / "analysis" / "human-calibration.md"
        if write_text(checklist_path, render_checklist(entry), overwrite=args.overwrite):
            written += 1

    print(f"prepared candidates={len(selected)} checklists_written={written} plan={plan_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
