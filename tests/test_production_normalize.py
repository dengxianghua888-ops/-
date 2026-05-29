import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from test_production_quality import add_common_production_artifacts, make_story_text, production_quality_report, write


def run_script(script, *args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_phase3_selected_candidate_object_normalizes_to_id(tmp_path):
    story = tmp_path / "story"
    add_common_production_artifacts(story, make_story_text(10500))
    room_path = story / "adaptation-room.json"
    room = json.loads(room_path.read_text(encoding="utf-8"))
    room["selected_candidate"] = {"id": "A", "premise": "遗嘱触发失踪亲属谜题"}
    write(room_path, json.dumps(room, ensure_ascii=False))

    result = run_script("production_normalize.py", "--story", story, "--phase", "3", "--mode", "production")

    assert result.returncode == 0, result.stderr
    normalized = json.loads(room_path.read_text(encoding="utf-8"))
    assert normalized["selected_candidate"] == "A"
    assert "selected_candidate_object_to_id" in result.stdout


def test_phase3_unknown_selected_candidate_id_still_fails_validation(tmp_path):
    story = tmp_path / "story"
    add_common_production_artifacts(story, make_story_text(10500))
    room_path = story / "adaptation-room.json"
    room = json.loads(room_path.read_text(encoding="utf-8"))
    room["selected_candidate"] = {"id": "missing", "premise": "不存在的候选"}
    write(room_path, json.dumps(room, ensure_ascii=False))

    normalize = run_script("production_normalize.py", "--story", story, "--phase", "3", "--mode", "production")
    validate = run_script("validate-production-story.py", "--story", story, "--phase", "3", "--mode", "production")

    assert normalize.returncode == 0, normalize.stderr
    assert validate.returncode != 0
    assert "selected_candidate must match a candidate id" in validate.stderr


def test_phase4_forbidden_summary_string_normalizes_but_empty_still_fails(tmp_path):
    story = tmp_path / "story"
    add_common_production_artifacts(story, make_story_text(10500))
    bible_path = story / "beat-bible.json"
    bible = json.loads(bible_path.read_text(encoding="utf-8"))
    bible["beats"][0]["forbidden_summary"] = "不能写成解释段"
    bible["beats"][1]["forbidden_summary"] = ""
    write(bible_path, json.dumps(bible, ensure_ascii=False))

    normalize = run_script("production_normalize.py", "--story", story, "--phase", "4", "--mode", "production")
    validate = run_script("validate-production-story.py", "--story", story, "--phase", "4", "--mode", "production")

    normalized = json.loads(bible_path.read_text(encoding="utf-8"))
    assert normalize.returncode == 0, normalize.stderr
    assert normalized["beats"][0]["forbidden_summary"] == ["不能写成解释段"]
    assert normalized["beats"][1]["forbidden_summary"] == ""
    assert validate.returncode != 0
    assert "beats[2].forbidden_summary must be a non-empty list" in validate.stderr


def test_phase6_scores_gate_and_machine_metrics_are_normalized(tmp_path):
    story = tmp_path / "story"
    final_text = make_story_text(10500)
    add_common_production_artifacts(story, final_text)
    report_path = story / "quality-report.json"
    report = production_quality_report(final_text=final_text)
    report["critic_scores"] = {"platform": 78, "emotion": 90, "style": 82, "logic": 64}
    report["machine_metrics"]["target_length"]["actual"] = 42
    write(report_path, json.dumps(report, ensure_ascii=False))
    write(story / "review.md", "# Critic Gauntlet Review\n\n## Gate Status: PASS\n")
    for name, score in {"platform": 78, "emotion": 90, "style": 82, "logic": 64}.items():
        write(story / "evaluation" / f"{name}.json", json.dumps({"status": "pass", "score": score, "evidence": [f"{name} evidence"]}, ensure_ascii=False))

    result = run_script("production_normalize.py", "--story", story, "--phase", "6", "--mode", "production")
    validate = run_script("validate-production-story.py", "--story", story, "--phase", "6", "--mode", "production", "--require-pass")

    normalized = json.loads(report_path.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert normalized["critic_scores"] == {"platform": 7.8, "emotion": 9.0, "style": 8.2, "logic": 6.4}
    assert normalized["machine_metrics"]["target_length"]["actual"] != 42
    assert (story / "review.md").read_text(encoding="utf-8").startswith("```yaml\ngate_status: pass")
    assert json.loads((story / "evaluation" / "platform.json").read_text(encoding="utf-8"))["score"] == 7.8
    assert validate.returncode != 0
    assert "pass gate requires critic_scores.logic >= 7" in validate.stderr


def test_phase6_normalizer_does_not_turn_fail_gate_into_pass(tmp_path):
    story = tmp_path / "story"
    final_text = make_story_text(10500)
    add_common_production_artifacts(story, final_text)
    report = production_quality_report(final_text=final_text)
    report["gate_status"] = "fail"
    report["critical_failures"] = [{"id": "logic", "issue": "证据链断裂"}]
    report["critic_scores"] = {"platform": 8, "emotion": 8, "style": 8, "logic": 6}
    write(story / "quality-report.json", json.dumps(report, ensure_ascii=False))
    write(story / "review.md", "# Critic Gauntlet Review\n\n## Gate Status: FAIL\n")

    result = run_script("production_normalize.py", "--story", story, "--phase", "6", "--mode", "production")

    normalized = json.loads((story / "quality-report.json").read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert normalized["gate_status"] == "fail"
    assert (story / "review.md").read_text(encoding="utf-8").startswith("```yaml\ngate_status: fail")
