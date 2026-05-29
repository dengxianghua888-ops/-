#!/usr/bin/env python3
"""Mock StoryForge runner for offline regression tests."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


def fixture_path(phase: int, fixture_dir: Path) -> Path:
    return fixture_dir / f"phase{phase}.bundle.txt"


def file_block(path: str, content: str) -> str:
    return f"<<<FILE: {path}>>>\n{content.rstrip()}\n<<<END FILE>>>\n"


def story_text(target: int = 10500) -> str:
    parts = []
    index = 1
    while sum(len(part) for part in parts) < target:
        parts.append(
            f"第{index:04d}场，闻夏拿起第{index:04d}份证据走到门口。"
            f"母亲伸手拦她，父亲按住文件，周律师把录音笔推过来。"
            f"她看着门缝里的光问：“第{index:04d}个答案，你们还要藏多久？”\n"
        )
        index += 1
    return "".join(parts)[:target]


def quality_report(mode: str) -> dict:
    min_chars = 6000 if mode == "ultra_short" else 10000
    max_chars = 9000 if mode == "ultra_short" else 18000
    actual = 7200 if mode == "ultra_short" else 10500
    return {
        "schema_version": 2,
        "pipeline_mode": mode,
        "gate_status": "pass",
        "critical_failures": [],
        "important_failures": [],
        "machine_metrics": {
            "target_length": {"min": min_chars, "max": max_chars, "actual": actual, "status": "pass"},
            "chapters": {"count": 0, "hook_coverage": 0, "status": "pass"},
            "paywall_cards": {"required": 3, "actual": 3, "status": "pass"},
            "source_overlap": {"max_continuous_overlap_chars": 0, "status": "pass"},
            "repeated_ngram": {"max_repeated_substring_chars": 0, "status": "pass"},
            "style_metrics": {"avg_sentence_length": 18, "dialogue_ratio": 0.35, "action_density_per_k": 12},
            "forbidden_words": {"hits": {}, "status": "pass"},
            "soft_forbidden_words": {"hits": {}, "status": "pass"},
        },
        "critic_scores": {"platform": 8, "emotion": 8, "style": 8, "logic": 8},
        "evidence": ["platform evidence", "emotion evidence", "style evidence", "logic evidence"],
    }


def production_bundle(phase: int, story_slug: str, mode: str) -> str | None:
    min_chars = 6000 if mode == "ultra_short" else 10000
    max_chars = 9000 if mode == "ultra_short" else 18000
    final_text = story_text(7200 if mode == "ultra_short" else 10500)
    actual = len(final_text)
    chapter_target = 800 if mode == "ultra_short" else 900

    if phase == 1:
        return file_block(
            "market-brief.json",
            json.dumps(
                {
                    "pipeline_mode": mode,
                    "target_platform": "tomato",
                    "target_length": {"min": min_chars, "max": max_chars},
                    "tomato_rules": {
                        "minimum_short_story_chars": 6000,
                        "best_range_chars": [10000, 30000],
                    },
                },
                ensure_ascii=False,
                indent=2,
            ),
        )
    if phase == 2:
        files = {
            "story-brief.json": json.dumps(
                {
                    "pipeline_mode": mode,
                    "genre": "family_ethics",
                    "reversal_mechanisms": ["inheritance_trigger", "missing_relative"],
                    "source_length_chars": 10,
                },
                ensure_ascii=False,
                indent=2,
            ),
            "dissection.md": "# Source Dissection\n\n开篇钩子、情绪债、反转机制已拆解。\n",
            "analysis/beat-sheet.md": "# Beat Sheet\n\n每 800-1200 字设置一个微钩。\n",
            "analysis/style-dna.md": "# Style DNA\n\n短句、动作优先、解释后置。\n",
            "analysis/soul-contract.md": "# Soul Contract\n\n读者期待主角拿回被隐藏的尊严与真相。\n",
            "analysis/reader-engine.md": "# Reader Engine\n\n点击欲来自遗嘱与失踪哥哥的信息差。\n",
            "analysis/tension-ledger.md": "# Tension Ledger\n\n每一场保留未偿情绪债。\n",
        }
        return "".join(file_block(path, content) for path, content in files.items())
    if phase == 3:
        files = {
            "adaptation.md": "# Adaptation Room\n\n选择高考前遗嘱触发的家庭伦理短故事变体。\n",
            "adaptation-room.json": json.dumps(
                {
                    "selected_candidate": "A",
                    "candidates": [
                        {
                            "id": "A",
                            "hook": "高考前一晚，遗嘱要求她找回失踪哥哥",
                            "risk": "父母转变过快",
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
        }
        return "".join(file_block(path, content) for path, content in files.items())
    if phase == 4:
        bible = {
            "pipeline_mode": mode,
            "target_length": {"min": min_chars, "max": max_chars},
            "beats": [
                {
                    "beat_id": "beat-01",
                    "target_chars": 3000,
                    "scene_location": "闻家客厅",
                    "character_goal": "拿到遗嘱和信托文件",
                    "conflict_action": "父亲按住文件，母亲挡住门",
                    "information_gap": "失踪哥哥到底是谁",
                    "emotion_debt_balance": "被忽视多年",
                    "chapter_end_hook": "门外传来哥哥的名字",
                    "paywall_card": True,
                    "forbidden_summary": ["不能写成家人解释前情"],
                },
                {
                    "beat_id": "beat-02",
                    "target_chars": 3500,
                    "scene_location": "律师事务所",
                    "character_goal": "验证录音和亲子报告",
                    "conflict_action": "哥哥抢走档案袋",
                    "information_gap": "遗嘱第二页被撕掉",
                    "emotion_debt_balance": "被替代的十八年",
                    "chapter_end_hook": "第二页写着她的真名",
                    "paywall_card": True,
                    "forbidden_summary": ["不能让律师一次讲完真相"],
                },
                {
                    "beat_id": "beat-03",
                    "target_chars": 4000,
                    "scene_location": "学校礼堂",
                    "character_goal": "在公开场合逼父母承认证据",
                    "conflict_action": "父亲夺话筒，母亲跪下求她闭嘴",
                    "information_gap": "哥哥失踪是被谁安排",
                    "emotion_debt_balance": "需要现场偿还",
                    "chapter_end_hook": "她把录音按下播放键",
                    "paywall_card": True,
                    "forbidden_summary": ["不能靠旁白完成情绪释放"],
                },
            ],
        }
        scene_card = {
            "scene_id": "scene-01",
            "beat_id": "beat-01",
            "target_chars_min": 800,
            "target_chars_max": 1200,
            "location": "闻家客厅",
            "time": "高考前夜",
            "pov": "first_person",
            "characters": ["闻夏", "父亲", "母亲", "周律师"],
            "character_goal": "拿到遗嘱和信托文件",
            "opposition_goal": "阻止她打开门",
            "conflict_action": "父亲按住文件，母亲挡住门",
            "information_gap": "失踪哥哥到底是谁",
            "emotional_debt_delta": "被忽视多年的情绪债继续加码",
            "payoff_or_hook": "门外传来哥哥的名字",
            "emotion_debt_balance": "被忽视多年",
            "chapter_end_hook": "门外传来哥哥的名字",
            "paywall_card": True,
            "must_include": ["遗嘱", "信托文件", "录音笔"],
            "must_not_write_as_exposition": ["不能用旁白解释哥哥身份"],
        }
        return "".join(
            [
                file_block("beat-bible.json", json.dumps(bible, ensure_ascii=False, indent=2)),
                file_block("scene-cards/scene-01.json", json.dumps(scene_card, ensure_ascii=False, indent=2)),
            ]
        )
    if phase == 5:
        return "".join(
            [
                file_block("draft-scenes/scene-01.md", final_text),
                file_block("draft.md", final_text),
            ]
        )
    if phase == 6:
        files = {
            "review.md": "# 审校报告\n\n```yaml\ngate_status: pass\ncritical_failures: []\nimportant_failures: []\n```\n",
            "quality-report.json": json.dumps(quality_report(mode), ensure_ascii=False, indent=2),
            "diff.md": "# Diff\n\nmock runner 无结构性返工。\n",
            "evaluation/platform.json": json.dumps({"status": "pass", "score": 8, "evidence": ["章末钩覆盖"]}, ensure_ascii=False),
            "evaluation/emotion.json": json.dumps({"status": "pass", "score": 8, "evidence": ["情绪债现场偿还"]}, ensure_ascii=False),
            "evaluation/style.json": json.dumps({"status": "pass", "score": 8, "evidence": ["动作密度达标"]}, ensure_ascii=False),
            "evaluation/logic.json": json.dumps({"status": "pass", "score": 8, "evidence": ["证据链闭合"]}, ensure_ascii=False),
        }
        return "".join(file_block(path, content) for path, content in files.items())
    if phase == 7:
        files = {
            "final.md": final_text,
            "craft-notes.md": "# Craft Notes\n\nproduction mock final packager artifact。\n",
            "tomato-submission.md": "# 投稿包\n\n## 标题 A\n高考前遗嘱让我找回失踪哥哥\n\n## 简介\n高考前一晚，闻夏收到遗嘱，发现父母藏了十八年的真相。\n\n## 标签\n家庭伦理 / 逆袭 / 遗嘱反转\n",
            "story.yaml": (
                f"slug: {story_slug}\n"
                f"pipeline_mode: {mode}\n"
                "target_platform: tomato\n"
                "genre: family_ethics\n"
                "status: final\n"
                "quality_gate:\n"
                "  gate_status: pass\n"
            ),
        }
        chapter_map = "| 章 | 字数 | 本章钩子 |\n|---|---:|---|\n"
        chapter_count = 9 if mode == "ultra_short" else 10
        for index in range(chapter_count):
            chapter = story_text(chapter_target + index)
            files[f"final-chapters/ch{index + 1:02d}.md"] = chapter
            chapter_map += f"| {index + 1:02d} | {len(chapter)} | 她问：“第{index + 1}扇门后是谁？” |\n"
        files["final-chapters/_chapters-map.md"] = chapter_map
        return "".join(file_block(path, content) for path, content in files.items())
    if phase == 8:
        return file_block(
            "feedback-learning.json",
            json.dumps(
                {
                    "story_slug": story_slug,
                    "pipeline_mode": mode,
                    "genre": "family_ethics",
                    "mechanisms": ["inheritance_trigger", "missing_relative"],
                    "target_length": {"min": min_chars, "max": max_chars},
                    "final_length": actual,
                    "failure_types": [],
                    "successful_hooks": ["遗嘱触发失踪亲属信息差"],
                    "paywall_cards": [{"beat_id": "beat-01"}, {"beat_id": "beat-02"}, {"beat_id": "beat-03"}],
                    "quality_scores": {"platform": 8, "emotion": 8, "style": 8, "logic": 8},
                    "new_forbidden_candidates": [],
                    "retrieval_tags": ["family_ethics", "inheritance_trigger", "missing_relative"],
                    "manual_revision_delta": [],
                },
                ensure_ascii=False,
                indent=2,
            ),
        )
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--phase", required=True, type=int)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--model", default="")
    parser.add_argument("--fixture-dir", default="")
    parser.add_argument("--mode", default="v4")
    args = parser.parse_args()

    started = time.time()
    run_dir = Path(args.run_dir)
    fixture_dir = args.fixture_dir or os.environ.get("STORYFORGE_MOCK_FIXTURE_DIR", "")
    mode = "ultra_short" if args.mode in {"ultra_short", "ultrashort", "short"} else "production" if args.mode in {"production", "prod"} else "v4"
    fixtures = Path(fixture_dir) if fixture_dir else Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "mock-runs"
    source = fixture_path(args.phase, fixtures)
    output = run_dir / f"phase{args.phase}.model.out"
    if mode in {"production", "ultra_short"} and not fixture_dir:
        builtin = production_bundle(args.phase, Path(args.story).name, mode)
        if builtin is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(builtin, encoding="utf-8")
            result = {
                "phase": args.phase,
                "runner": "mock",
                "provider": "mock",
                "status": "success",
                "exit_code": 0,
                "model_or_command": f"builtin-{mode}-fixture",
                "duration_s": round(time.time() - started, 3),
                "output_bundle": str(output),
                "artifacts_written": [],
                "failure_reason": "",
            }
            print(json.dumps(result, ensure_ascii=False))
            return 0
    if not source.exists():
        result = {
            "phase": args.phase,
            "runner": "mock",
            "provider": "mock",
            "status": "failed",
            "exit_code": 22,
            "model_or_command": "fixture",
            "duration_s": round(time.time() - started, 3),
            "output_bundle": str(output),
            "artifacts_written": [],
            "failure_reason": f"missing mock fixture: {source}",
        }
        print(json.dumps(result, ensure_ascii=False))
        return 22

    output.parent.mkdir(parents=True, exist_ok=True)
    fixture_text = source.read_text(encoding="utf-8").replace("{{STORY_SLUG}}", Path(args.story).name)
    output.write_text(fixture_text, encoding="utf-8")
    result = {
        "phase": args.phase,
        "runner": "mock",
        "provider": "mock",
        "status": "success",
        "exit_code": 0,
        "model_or_command": "fixture",
        "duration_s": round(time.time() - started, 3),
        "output_bundle": str(output),
        "artifacts_written": [],
        "failure_reason": "",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
