import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PHASE_ALIASES = {
    "phase1": "phase1",
    "phase2": "phase2",
    "draft": "phase3",
    "review": "phase4",
    "final": "phase5",
}


def run_script(script, *args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
        cwd=cwd,
        text=True,
        capture_output=True,
    )


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_template_required_artifacts(path):
    data = {}
    current = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("  ") and raw.strip().endswith(":"):
            current = raw.strip()[:-1]
            data[current] = []
        elif current and raw.strip().startswith("- "):
            data[current].append(raw.strip()[2:])
    return data


def minimal_final_story(tmp_path):
    story = tmp_path / "story"
    for rel in [
        "source.md",
        "dissection.md",
        "analysis/beat-sheet.md",
        "analysis/style-dna.md",
        "analysis/characters.md",
        "analysis/theme.md",
        "analysis/soul-contract.md",
        "analysis/reader-engine.md",
        "analysis/tension-ledger.md",
        "analysis/platform-fit.md",
        "adaptation.md",
        "blueprint.md",
        "draft.md",
        "diff.md",
        "final.md",
        "craft-notes.md",
        "tomato-submission.md",
        "final-chapters/_chapters-map.md",
    ]:
        write(story / rel, f"# {rel}\n")
    write(
        story / "story.yaml",
        "slug: story\ntarget_platform: tomato\ngenre: modern_reversal\nstatus: final\nquality_gate:\n  gate_status: pass\n",
    )
    write(
        story / "review.md",
        """# 审校报告

```yaml
gate_status: pass
critical_failures: []
important_failures: []
```
""",
    )
    write(
        story / "quality-report.json",
        json.dumps(
            {
                "gate_status": "pass",
                "critical_failures": [],
                "important_failures": [],
                "hard_checks": {"required_artifacts": "pass"},
                "mechanism_fidelity": {"status": "pass", "items": []},
                "soul_fidelity": {"status": "pass", "items": []},
            },
            ensure_ascii=False,
        ),
    )
    return story


def test_validate_quality_report_accepts_structured_pass(tmp_path):
    story = minimal_final_story(tmp_path)

    result = run_script("validate-quality-report.py", "--story", story)

    assert result.returncode == 0, result.stderr
    assert "gate_status=pass" in result.stdout


def test_validate_quality_report_rejects_pass_with_nested_critical_fail(tmp_path):
    story = minimal_final_story(tmp_path)
    report = json.loads((story / "quality-report.json").read_text(encoding="utf-8"))
    report["soul_fidelity"] = {
        "status": "fail",
        "items": [{"contract_item": "读者承诺", "status": "fail", "evidence": "missing"}],
    }
    write(story / "quality-report.json", json.dumps(report, ensure_ascii=False))

    result = run_script("validate-quality-report.py", "--story", story)

    assert result.returncode != 0
    assert "failing critical checks" in result.stderr


def test_validate_quality_report_rejects_malformed_nested_section(tmp_path):
    story = minimal_final_story(tmp_path)
    report = json.loads((story / "quality-report.json").read_text(encoding="utf-8"))
    report["mechanism_fidelity"] = {"items": []}
    write(story / "quality-report.json", json.dumps(report, ensure_ascii=False))

    result = run_script("validate-quality-report.py", "--story", story)

    assert result.returncode != 0
    assert "mechanism_fidelity.status" in result.stderr


def test_validate_quality_report_rejects_missing_review_gate(tmp_path):
    story = minimal_final_story(tmp_path)
    write(story / "review.md", "# 审校报告\n\nPASS ✅\n")

    result = run_script("validate-quality-report.py", "--story", story)

    assert result.returncode != 0
    assert "machine-readable gate" in result.stderr


def test_validate_quality_report_accepts_multiline_failure_lists(tmp_path):
    story = minimal_final_story(tmp_path)
    write(
        story / "review.md",
        """# 审校报告

```yaml
gate_status: fail
critical_failures:
  - C0 神髓禁改项丢失
important_failures:
  - I5 缺章末钩子
```
""",
    )
    report = json.loads((story / "quality-report.json").read_text(encoding="utf-8"))
    report["gate_status"] = "fail"
    report["critical_failures"] = ["C0 神髓禁改项丢失"]
    report["important_failures"] = ["I5 缺章末钩子"]
    write(story / "quality-report.json", json.dumps(report, ensure_ascii=False))

    result = run_script("validate-quality-report.py", "--story", story)

    assert result.returncode == 0, result.stderr
    assert "gate_status=fail" in result.stdout


def test_validate_quality_report_require_pass_rejects_structured_fail(tmp_path):
    story = minimal_final_story(tmp_path)
    write(
        story / "review.md",
        """# 审校报告

```yaml
gate_status: fail
critical_failures:
  - C0 神髓禁改项丢失
important_failures: []
```
""",
    )
    report = json.loads((story / "quality-report.json").read_text(encoding="utf-8"))
    report["gate_status"] = "fail"
    report["critical_failures"] = ["C0 神髓禁改项丢失"]
    write(story / "quality-report.json", json.dumps(report, ensure_ascii=False))

    result = run_script("validate-quality-report.py", "--story", story, "--require-pass")

    assert result.returncode != 0
    assert "quality gate failed" in result.stderr


def test_validate_quality_report_rejects_important_mismatch(tmp_path):
    story = minimal_final_story(tmp_path)
    report = json.loads((story / "quality-report.json").read_text(encoding="utf-8"))
    report["important_failures"] = ["I1 节奏偏差"]
    write(story / "quality-report.json", json.dumps(report, ensure_ascii=False))

    result = run_script("validate-quality-report.py", "--story", story)

    assert result.returncode != 0
    assert "important_failures" in result.stderr


def test_validate_story_requires_soul_contract_for_final(tmp_path):
    story = minimal_final_story(tmp_path)
    (story / "analysis" / "soul-contract.md").unlink()

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode != 0
    assert "analysis/soul-contract.md" in result.stderr


def test_validate_story_requires_diff_for_final(tmp_path):
    story = minimal_final_story(tmp_path)
    (story / "diff.md").unlink()

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode != 0
    assert "diff.md" in result.stderr


def test_validate_story_rejects_story_yaml_status_drift(tmp_path):
    story = minimal_final_story(tmp_path)
    write(
        story / "story.yaml",
        "slug: story\ntarget_platform: tomato\ngenre: modern_reversal\nstatus: draft\nquality_gate:\n  gate_status: pass\n",
    )

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode != 0
    assert "status must be final or submitted" in result.stderr


def test_validate_story_phase5_alias_runs_final_semantic_checks(tmp_path):
    story = minimal_final_story(tmp_path)
    write(
        story / "story.yaml",
        "slug: story\ntarget_platform: tomato\ngenre: modern_reversal\nstatus: draft\nquality_gate:\n  gate_status: pass\n",
    )

    result = run_script("validate-story.py", "--story", story, "--phase", "phase5")

    assert result.returncode != 0
    assert "status must be final or submitted" in result.stderr


def test_validate_story_rejects_unknown_phase(tmp_path):
    story = minimal_final_story(tmp_path)

    result = run_script("validate-story.py", "--story", story, "--phase", "phase6")

    assert result.returncode != 0
    assert "unknown phase" in result.stderr


def test_validate_story_rejects_final_with_hard_forbidden_word(tmp_path):
    story = minimal_final_story(tmp_path)
    write(story / "final.md", "然而我还是拿着证据走进大厅。\n")

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode != 0
    assert "hard forbidden words" in result.stderr


def test_validate_story_rejects_overlong_output_title(tmp_path):
    story = minimal_final_story(tmp_path)
    write(
        story / "story.yaml",
        "slug: story\ntarget_platform: tomato\ngenre: modern_reversal\nstatus: final\noutput_title: 这是一个超过三十个汉字的番茄标题肯定需要被机器质量门拦下来否则会出问题\nquality_gate:\n  gate_status: pass\n",
    )

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode != 0
    assert "output_title exceeds 30 chars" in result.stderr


def test_validate_story_rejects_genre_specific_forbidden_word(tmp_path):
    story = minimal_final_story(tmp_path)
    write(
        story / "story.yaml",
        "slug: story\ntarget_platform: tomato\ngenre: ancient_BE\nstatus: final\nquality_gate:\n  gate_status: pass\n",
    )
    write(story / "final.md", "我把手机放在案上，看他跪在雪里。\n")

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode != 0
    assert "手机" in result.stderr


@pytest.mark.skipif(
    not (ROOT / "stories" / "hermes_bag" / "source.md").exists(),
    reason="copyrighted source fixture is local-only",
)
def test_hermes_bag_v4_golden_case_validates():
    story = ROOT / "stories" / "hermes_bag"

    result = run_script("validate-story.py", "--story", story, "--phase", "final")

    assert result.returncode == 0, result.stderr


def test_check_style_metrics_reports_forbidden_and_soft_terms(tmp_path):
    story = tmp_path / "story"
    write(story / "final.md", "然而我只是淡淡地看着他。\n“凭什么？”\n")

    result = run_script("check-style-metrics.py", "--story", story, "--json")

    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["forbidden_hits"]["然而"] == 1
    assert data["soft_forbidden_hits"]["淡淡"] == 1
    assert data["question_marks"] == 1


def test_repair_style_stats_normalizes_percent_dialogue_ratio(tmp_path):
    stats = tmp_path / "style-dna-stats.json"
    write(
        stats,
        json.dumps(
            {
                "by_genre": {
                    "modern_reversal": {
                        "dialogue_ratio": {
                            "mean": 20.2,
                            "std": 28.001,
                            "n": 2,
                            "samples": [40.0, 0.4],
                        }
                    }
                }
            },
            ensure_ascii=False,
        ),
    )

    result = run_script("repair-style-stats.py", "--stats", stats)

    assert result.returncode == 0, result.stderr
    data = json.loads(stats.read_text(encoding="utf-8"))
    ratio = data["by_genre"]["modern_reversal"]["dialogue_ratio"]
    assert ratio["samples"] == [0.4, 0.4]
    assert ratio["mean"] == 0.4


def test_update_corpus_index_exports_v4_gene_fields(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(story / "source.md", "原文")
    write(
        story / "dissection.md",
        """genre: modern_reversal
genre_confidence: high

## 题材与机制(V3 新增)
- **title_formula**: T1
- **reversal_mechanisms**: [M1, M3]
- **hook_type**: H1
- **emotion_curve_shape**: U型
""",
    )
    write(
        story / "analysis" / "soul-contract.md",
        """**一句话承诺**: 看主角用对方规则反杀。
**情绪债**: 公开羞辱债
**反派必须被惩罚的理由**: 滥用权力。
**核心姿态**: 冷静隐忍
**最终必须兑现的体验**: 规则回旋清算
""",
    )
    write(story / "analysis" / "reader-engine.md", "**主要爽点**: 死环反杀\n")
    write(story / "analysis" / "platform-fit.md", "**总分**: 8.5\n")

    result = run_script("update-corpus-index.py", "--corpus", corpus)

    assert result.returncode == 0, result.stderr
    index = json.loads((corpus / "_index.json").read_text(encoding="utf-8"))
    entry = index["entries"][0]
    assert entry["reader_promise"] == "看主角用对方规则反杀。"
    assert entry["dominant_s爽点"] == "死环反杀"
    assert entry["tomato_fit_score"] == 8.5


def test_update_corpus_index_extracts_debt_type_from_template_table(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(
        story / "dissection.md",
        """genre: family_ethics
genre_confidence: high
- **reversal_mechanisms**: [M3]
""",
    )
    write(
        story / "analysis" / "soul-contract.md",
        """**一句话承诺**: 看背叛者被公开清算。
**反派必须被惩罚的理由**: 利用亲情绑架。
**核心姿态**: 冷硬拒绝和稀泥
**最终必须兑现的体验**: 同态报应

| 债务来源 | 承载 Beat | 读者情绪 | 必须如何偿还 |
|----------|-----------|----------|--------------|
| 亲情背叛债 | Beat 2-4 | 憋屈、愤怒 | 公开清算 |
""",
    )
    write(story / "analysis" / "reader-engine.md", "**主要爽点**: 因果回旋反讽\n")
    write(story / "analysis" / "platform-fit.md", "**总分**: 8.4\n")

    result = run_script("update-corpus-index.py", "--corpus", corpus)

    assert result.returncode == 0, result.stderr
    entry = json.loads((corpus / "_index.json").read_text(encoding="utf-8"))["entries"][0]
    assert entry["emotional_debt_type"] == "亲情背叛债"


def test_backfill_v4_analysis_generates_machine_draft_genes(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(
        corpus / "_index.json",
        json.dumps(
            {
                "_meta": {"description": "test index"},
                "entries": [
                    {
                        "slug": "case_one",
                        "status": "dissected",
                        "filename": "case.txt",
                        "word_count": 10000,
                        "genre": "modern_reversal",
                        "title_formula": "T1",
                        "reversal_mechanisms": ["M1", "M3"],
                        "hook_type": "H1",
                        "emotion_curve_shape": "U型",
                    }
                ],
            },
            ensure_ascii=False,
        ),
    )
    write(
        story / "dissection.md",
        """genre: modern_reversal
genre_confidence: high

## 题材与机制(V3 新增)
- **title_formula**: T1
- **reversal_mechanisms**: [M1, M3]
- **hook_type**: H1
- **emotion_curve_shape**: U型

## 全文概述
主角被规则压迫后，拿到盖章凭证反杀。
""",
    )

    result = run_script("backfill-v4-analysis.py", "--corpus", corpus, "--slug", "case_one")

    assert result.returncode == 0, result.stderr
    assert (story / "analysis" / "soul-contract.md").exists()
    assert (story / "analysis" / "reader-engine.md").exists()
    assert (story / "analysis" / "tension-ledger.md").exists()
    assert (story / "analysis" / "platform-fit.md").exists()

    result = run_script("update-corpus-index.py", "--corpus", corpus)
    assert result.returncode == 0, result.stderr
    index = json.loads((corpus / "_index.json").read_text(encoding="utf-8"))
    entry = index["entries"][0]
    assert entry["reader_promise"]
    assert entry["dominant_s爽点"] == "死环反杀"
    assert entry["v4_calibration_status"] == "machine_draft"


def test_backfill_v4_analysis_preserves_existing_artifacts_without_overwrite(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(
        corpus / "_index.json",
        json.dumps(
            {
                "entries": [
                    {
                        "slug": "case_one",
                        "status": "dissected",
                        "genre": "modern_reversal",
                        "reversal_mechanisms": ["M1"],
                    }
                ]
            },
            ensure_ascii=False,
        ),
    )
    write(story / "dissection.md", "genre: modern_reversal\n- **reversal_mechanisms**: [M1]\n")
    write(story / "analysis" / "soul-contract.md", "SENTINEL\n")

    result = run_script("backfill-v4-analysis.py", "--corpus", corpus, "--slug", "case_one")

    assert result.returncode == 0, result.stderr
    assert (story / "analysis" / "soul-contract.md").read_text(encoding="utf-8") == "SENTINEL\n"

    result = run_script("backfill-v4-analysis.py", "--corpus", corpus, "--slug", "case_one", "--overwrite")

    assert result.returncode == 0, result.stderr
    assert "SENTINEL" not in (story / "analysis" / "soul-contract.md").read_text(encoding="utf-8")


def test_corpus_health_reports_gene_completion_and_calibration_status(tmp_path):
    index = tmp_path / "_index.json"
    write(
        index,
        json.dumps(
            {
                "entries": [
                    {
                        "slug": "complete_case",
                        "status": "dissected",
                        "genre": "modern_reversal",
                        "reversal_mechanisms": ["M1"],
                        "reader_promise": "promise",
                        "emotional_debt_type": "debt",
                        "dominant_s爽点": "死环反杀",
                        "antagonist_violation": "violation",
                        "protagonist_stance": "stance",
                        "payoff_pattern": "payoff",
                        "tomato_fit_score": 8.5,
                        "v4_calibration_status": "machine_draft",
                    },
                    {
                        "slug": "missing_case",
                        "status": "dissected",
                        "genre": "family_ethics",
                        "reversal_mechanisms": ["M3"],
                    },
                    {"slug": "pending_case", "status": "pending"},
                ]
            },
            ensure_ascii=False,
        ),
    )

    result = run_script("corpus-health.py", "--index", index, "--json")

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["gene_complete"] == 1
    assert report["machine_draft_genes"] == ["complete_case"]
    assert report["missing_genes"] == ["missing_case"]
    modern = report["human_calibration"]["by_genre"]["modern_reversal"]
    assert modern["available"] == 1
    assert modern["available_target"] == 1
    assert modern["calibrated"] == 0
    assert modern["deficit"] == 1


def test_prepare_human_calibration_creates_plan_and_checklists(tmp_path):
    corpus = tmp_path / "corpus"
    entries = [
        {
            "slug": "modern_high",
            "status": "dissected",
            "genre": "modern_reversal",
            "filename": "modern_high.txt",
            "word_count": 10000,
            "reversal_mechanisms": ["M1", "M3"],
            "reader_promise": "promise",
            "emotional_debt_type": "debt",
            "dominant_s爽点": "死环反杀",
            "antagonist_violation": "violation",
            "protagonist_stance": "stance",
            "payoff_pattern": "payoff",
            "tomato_fit_score": 8.8,
            "v4_calibration_status": "machine_draft",
        },
        {
            "slug": "modern_low",
            "status": "dissected",
            "genre": "modern_reversal",
            "filename": "modern_low.txt",
            "word_count": 9000,
            "reversal_mechanisms": ["M1"],
            "reader_promise": "promise",
            "emotional_debt_type": "debt",
            "dominant_s爽点": "死环反杀",
            "antagonist_violation": "violation",
            "protagonist_stance": "stance",
            "payoff_pattern": "payoff",
            "tomato_fit_score": 7.8,
            "v4_calibration_status": "machine_draft",
        },
        {
            "slug": "family_case",
            "status": "dissected",
            "genre": "family_ethics",
            "filename": "family.txt",
            "word_count": 9500,
            "reversal_mechanisms": ["M3"],
            "reader_promise": "promise",
            "emotional_debt_type": "debt",
            "dominant_s爽点": "因果回旋反讽",
            "antagonist_violation": "violation",
            "protagonist_stance": "stance",
            "payoff_pattern": "payoff",
            "tomato_fit_score": 8.2,
            "v4_calibration_status": "machine_draft",
        },
    ]
    write(corpus / "_index.json", json.dumps({"entries": entries}, ensure_ascii=False))
    for entry in entries:
        write(corpus / entry["slug"] / "dissection.md", "# dissection\n")

    result = run_script("prepare-human-calibration.py", "--corpus", corpus, "--per-genre", "1")

    assert result.returncode == 0, result.stderr
    plan = (corpus / "_human-calibration-plan.md").read_text(encoding="utf-8")
    assert "modern_high" in plan
    assert "family_case" in plan
    assert "modern_low" not in plan
    checklist = (corpus / "modern_high" / "analysis" / "human-calibration.md").read_text(encoding="utf-8")
    assert "decision: pending" in checklist
    assert 'reviewer: ""' in checklist
    assert "machine_draft" in checklist


def test_apply_human_calibration_requires_approved_completed_checklist(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(
        story / "analysis" / "soul-contract.md",
        "# soul\n\n**v4_calibration_status**: machine_draft\n",
    )
    write(
        story / "analysis" / "reader-engine.md",
        "# reader\n\n**v4_calibration_status**: machine_draft\n",
    )
    write(
        story / "analysis" / "tension-ledger.md",
        "# tension\n\n**v4_calibration_status**: machine_draft\n",
    )
    write(
        story / "analysis" / "platform-fit.md",
        "# platform\n\n**v4_calibration_status**: machine_draft\n",
    )
    write(
        story / "analysis" / "human-calibration.md",
        """# V4 人工校准清单

```yaml
slug: case_one
reviewer: "DXH"
reviewed_at: "2026-04-26"
decision: approved
```

- [x] 读完 `dissection.md`
- [x] 确认 dominant_s爽点

reader_promise: human promise
emotional_debt_type: human debt
dominant_s爽点: 身份反差爆发
antagonist_violation: human violation
protagonist_stance: human stance
payoff_pattern: human payoff
tomato_fit_score: 8.6
""",
    )

    result = run_script("apply-human-calibration.py", "--corpus", corpus, "--slug", "case_one")

    assert result.returncode == 0, result.stderr
    for rel in [
        "analysis/soul-contract.md",
        "analysis/reader-engine.md",
        "analysis/tension-ledger.md",
        "analysis/platform-fit.md",
    ]:
        text = (story / rel).read_text(encoding="utf-8")
        assert "**v4_calibration_status**: human_calibrated" in text
        assert "**v4_human_reviewer**: DXH" in text
        assert "V4_HUMAN_CALIBRATION_START" in text
        assert "human promise" in text


def test_apply_human_calibration_rejects_unchecked_items(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(story / "analysis" / "soul-contract.md", "**v4_calibration_status**: machine_draft\n")
    write(
        story / "analysis" / "human-calibration.md",
        """```yaml
slug: case_one
reviewer: "DXH"
reviewed_at: "2026-04-26"
decision: approved
```

- [ ] 还没读完 dissection
""",
    )

    result = run_script("apply-human-calibration.py", "--corpus", corpus, "--slug", "case_one")

    assert result.returncode != 0
    assert "unchecked checklist" in result.stderr


def test_update_corpus_index_prefers_approved_human_calibration_fields(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(
        story / "dissection.md",
        """genre: apocalypse_heroine
genre_confidence: high
- **reversal_mechanisms**: [M2, M7]
""",
    )
    write(
        story / "analysis" / "soul-contract.md",
        """**v4_calibration_status**: human_calibrated
**一句话承诺**: machine promise
**情绪债**: machine debt
**反派必须被惩罚的理由**: machine violation
**核心姿态**: machine stance
**最终必须兑现的体验**: machine payoff
""",
    )
    write(story / "analysis" / "reader-engine.md", "**主要爽点**: 降维打击\n")
    write(story / "analysis" / "platform-fit.md", "**总分**: 8.0\n")
    write(
        story / "analysis" / "human-calibration.md",
        """```yaml
slug: case_one
reviewer: "Codex"
reviewed_at: "2026-04-27"
decision: approved
```

reader_promise: human promise
emotional_debt_type: human debt
dominant_s爽点: 身份反差爆发
antagonist_violation: human violation
protagonist_stance: human stance
payoff_pattern: human payoff
tomato_fit_score: 8.6
""",
    )

    result = run_script("update-corpus-index.py", "--corpus", corpus)

    assert result.returncode == 0, result.stderr
    entry = json.loads((corpus / "_index.json").read_text(encoding="utf-8"))["entries"][0]
    assert entry["reader_promise"] == "human promise"
    assert entry["dominant_s爽点"] == "身份反差爆发"
    assert entry["tomato_fit_score"] == 8.6


def test_update_corpus_index_rejects_incomplete_approved_human_calibration(tmp_path):
    corpus = tmp_path / "corpus"
    story = corpus / "case_one"
    write(
        story / "dissection.md",
        """genre: modern_reversal
genre_confidence: high
- **reversal_mechanisms**: [M1]
""",
    )
    write(story / "analysis" / "soul-contract.md", "**一句话承诺**: machine promise\n")
    write(
        story / "analysis" / "human-calibration.md",
        """```yaml
slug: case_one
reviewer: "Codex"
reviewed_at: "2026-04-27"
decision: approved
```

reader_promise: human promise
""",
    )

    result = run_script("update-corpus-index.py", "--corpus", corpus)

    assert result.returncode != 0
    assert "missing fields" in result.stderr


def test_story_manifest_template_required_artifacts_match_validator():
    sys.path.insert(0, str(ROOT / "scripts"))
    from v4_quality import required_artifacts_for_phase

    required = parse_template_required_artifacts(ROOT / "templates" / "story-manifest-template.yaml")
    for validator_phase, template_phase in PHASE_ALIASES.items():
        assert required[template_phase] == required_artifacts_for_phase(validator_phase)
