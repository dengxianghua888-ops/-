import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))

from test_production_quality import add_common_production_artifacts, make_story_text, write


def run_script(script, *args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_stability_report_writes_markdown_and_json(tmp_path):
    story = tmp_path / "story"
    add_common_production_artifacts(story, make_story_text(10500))
    run_dir = story / "runs" / "run1"
    write(
        run_dir / "execution-summary.md",
        "\n".join(
            [
                "# Execution Summary",
                "",
                "| Phase | Status | Started | Ended | Duration | Retries | Runner | Provider | Notes |",
                "|-------|--------|---------|-------|----------|---------|--------|----------|-------|",
                "| 3 | completed | 2026-05-09 00:00:00 | 2026-05-09 00:00:03 | 3s | 0 | mock | mock | 2 artifacts ok |",
                "| 4 | failed | 2026-05-09 00:00:03 | 2026-05-09 00:00:06 | 3s | 0 | mock | mock | validator failed |",
            ]
        )
        + "\n",
    )
    write(run_dir / "phase4.normalizer.log", json.dumps({"changes": ["forbidden_summary_string_to_list"]}, ensure_ascii=False))
    write(run_dir / "phase4.validator.log", json.dumps({"status": "fail", "failures": ["beat-bible schema"]}, ensure_ascii=False))
    out = tmp_path / "stability.md"

    result = run_script("production_stability_report.py", "--stories", story, "--out", out)

    assert result.returncode == 0, result.stderr
    markdown = out.read_text(encoding="utf-8")
    payload = json.loads(out.with_suffix(".json").read_text(encoding="utf-8"))
    assert "StoryForge Production Stability Report" in markdown
    assert "forbidden_summary_string_to_list" in markdown
    assert payload["stories"][0]["story"] == str(story)
    assert payload["stories"][0]["runs"][0]["phases"][1]["status"] == "failed"
