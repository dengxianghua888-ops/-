"""Source authorization, V6 role gates and failure-atomic publication regressions."""
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
# These imports intentionally follow the repository script-path setup.

import storyforge  # noqa: E402
import storyforge_lib as lib  # noqa: E402
from production_normalize import normalize_story  # noqa: E402
from production_quality import machine_evaluate  # noqa: E402
from test_production_quality import add_common_production_artifacts, make_story_text, write_bundle  # noqa: E402
from test_storyforge_runner import run_storyforge, write  # noqa: E402


def block(files):
    return "".join(f"<<<FILE: {p}>>>\n{v}\n<<<END FILE>>>\n" for p, v in files.items())


def tree_bytes(story):
    return {str(p.relative_to(story)): p.read_bytes() for p in story.rglob("*")
            if p.is_file() and "runs" not in p.relative_to(story).parts}


def test_gate_approval_preserves_source_policy_and_automation(tmp_path):
    story = tmp_path / "story"
    write(story / "source.md", "private source")
    original = {"slug": "story", "source_policy": {"access": "denied", "notes": "owner only"},
                "automation": {"runner": "agent", "current_phase": 3, "custom": "keep",
                               "human_gates": {"another_gate": "pending"}}}
    write(story / "story.yaml", yaml.safe_dump(original))
    result = run_storyforge("approve-gate", "--story", story, "--gate", "phase2_blueprint_review")
    assert result.returncode == 0
    after = yaml.safe_load((story / "story.yaml").read_text())
    assert after["source_policy"] == original["source_policy"]
    assert after["automation"] == original["automation"] | {"human_gates": {
        "another_gate": "pending", "phase2_blueprint_review": "approved"}}
    result = run_storyforge("run", "--story", story, "--runner", "agent")
    assert result.returncode == 30


@pytest.mark.parametrize("mode,critic,final", [("v4",4,5), ("production",6,7),
                                              ("ultra_short",6,7), ("production_v6",7,8)])
def test_role_coordinates(mode, critic, final):
    assert lib.phase_for_role(mode, "critic") == critic
    assert lib.phase_for_role(mode, "final") == final


def test_v6_rejects_unlisted_source_before_writes(tmp_path):
    story = tmp_path / "story"
    write(story / "source.md", "original")
    before = tree_bytes(story)
    with pytest.raises(ValueError, match="not allowed"):
        lib.apply_artifact_bundle(story, 1, block({"market-brief.json": "{}", "source.md": "bad"}),
                                  story / "runs" / "r", mode="production_v6")
    assert tree_bytes(story) == before


def test_second_candidate_write_failure_retains_live_bytes(tmp_path, monkeypatch):
    story = tmp_path / "story"
    write(story / "draft.md", "old draft")
    write(story / "draft-scenes/old.md", "old scene")
    before = tree_bytes(story)
    original = lib.write_text
    def fail_second(path, text):
        if path.name == "draft.md" and ".attempt-" in str(path):
            raise OSError("injected write failure")
        original(path, text)
    monkeypatch.setattr(lib, "write_text", fail_second)
    with pytest.raises(OSError, match="injected"):
        lib.apply_artifact_bundle(story, 6, block({"draft-scenes/new.md": "new", "draft.md": "new"}),
                                  story / "runs" / "r", mode="production_v6")
    assert tree_bytes(story) == before


def test_stale_outputs_replaced_and_attempt_backups_unique(tmp_path):
    story = tmp_path / "story"
    write(story / "draft.md", "first")
    write(story / "draft-scenes/old.md", "old")
    for text in ["second", "third"]:
        lib.apply_artifact_bundle(story, 6, block({"draft-scenes/new.md": text, "draft.md": text}),
                                  story / "runs/r", mode="production_v6")
    assert not (story / "draft-scenes/old.md").exists()
    backups = list(tmp_path.glob(".story.attempt-*/story/draft.md"))
    assert sorted(p.read_text().strip() for p in backups) == ["first", "second"]
    assert (story / "draft.md").read_text().strip() == "third"


def test_unsupported_atomic_exchange_fails_without_publication(tmp_path, monkeypatch):
    story = tmp_path / "story"
    write(story / "draft.md", "old")
    with lib.StagedStory(story, story / "runs/r", 6) as stage:
        write(stage.path / "draft.md", "candidate")
        monkeypatch.setattr(lib.sys, "platform", "unsupported")
        with pytest.raises(OSError, match="Atomic story exchange"):
            stage.publish()
    assert (story / "draft.md").read_text() == "old"


def test_v6_critic_reads_current_draft_and_does_not_finalize(tmp_path):
    story = tmp_path / "story"
    add_common_production_artifacts(story, make_story_text())
    write(story / "story.yaml", "slug: story\nstatus: phase6\n")
    write(story / "final.md", "stale final")
    metrics = machine_evaluate(story, 7, "production_v6")
    assert metrics["text_path"].endswith("draft.md")
    assert metrics["chapters"]["count"] == 0
    normalize_story(story, 7, "production_v6")
    assert yaml.safe_load((story / "story.yaml").read_text())["status"] == "phase6"
    assert (story / "final.md").read_text() == "stale final"


def v6_fixtures(tmp_path):
    template = tmp_path / "template"
    add_common_production_artifacts(template, make_story_text())
    write(template / "analysis/chapter-soul-map.json", "{}")
    write(template / "hook/opening-hook.md", "导语：证据忽然被送到门口。")
    write(template / "hook/hook-meta.json", "{}")
    bible = json.loads((template / "beat-bible.json").read_text())
    bible["chapters"] = [{"chapter_id": "c1", "scenes": ["scene-01"], "target_char_count": [10000, 18000]}]
    write(template / "beat-bible.json", json.dumps(bible))
    market = json.loads((template / "market-brief.json").read_text())
    market["pipeline_mode"] = "production_v6"
    write(template / "market-brief.json", json.dumps(market))
    write(template / "feedback-learning.json", json.dumps({"story_slug":"story", "pipeline_mode":"production_v6",
          "failure_types":[], "successful_hooks":[], "manual_revision_delta":[],
          "quality_scores": {k:8 for k in ["platform","emotion","style","logic"]}}))
    fixtures = tmp_path / "fixtures"
    for phase in range(1, 10):
        files = {}
        for pattern in lib.load_phase_bundle(phase, mode="production_v6").required_outputs:
            for path in template.glob(pattern):
                files[str(path.relative_to(template))] = path.read_text()
        write_bundle(fixtures / f"phase{phase}.bundle.txt", files)
    return fixtures


def test_v6_full_mock_from_empty_final_and_current_final_rubric(tmp_path):
    fixtures = v6_fixtures(tmp_path)
    story = tmp_path / "story"
    write(story / "source.md", "合成测试原文")
    result = run_storyforge("run", "--story", story, "--runner", "mock", "--mode", "production_v6",
                           "--run-id", "full", "--max-retries", 0, "--no-human-gates",
                           env={"STORYFORGE_MOCK_FIXTURE_DIR": str(fixtures)})
    assert result.returncode == 0, result.stderr + result.stdout + (story / "runs/full/execution-summary.md").read_text()
    assert (story / "runs/full/phase8.rubric.log").exists()
    assert not (story / "runs/full/phase7.rubric.log").exists()
    assert yaml.safe_load((story / "story.yaml").read_text())["status"] == "test_fixture"
    assert json.loads((story / "runs/full/run-manifest.json").read_text())["last_completed_phase"] == 9


def test_v6_critic_fail_cannot_publish_or_reach_final(tmp_path):
    fixtures = v6_fixtures(tmp_path)
    files = lib.parse_artifact_bundle((fixtures / "phase7.bundle.txt").read_text())
    report = json.loads(files["quality-report.json"])
    report["gate_status"] = "fail"
    files["quality-report.json"] = json.dumps(report)
    write_bundle(fixtures / "phase7.bundle.txt", files)
    story = tmp_path / "story"
    write(story / "source.md", "合成测试原文")
    result = run_storyforge("run", "--story", story, "--runner", "mock", "--mode", "production_v6",
                           "--run-id", "fail", "--max-retries", 0, "--no-human-gates",
                           env={"STORYFORGE_MOCK_FIXTURE_DIR": str(fixtures)})
    assert result.returncode == 23
    assert "quality gate failed" in (story / "runs/fail/phase7.validator.log").read_text()
    assert not (story / "quality-report.json").exists()
    assert not (story / "final.md").exists()
    assert not (story / "runs/fail/phase8.runner.log").exists()


def test_model_story_metadata_cannot_change_source_permission(tmp_path):
    story = tmp_path / "story"
    write(story / "story.yaml", "source_policy:\n  access: 'denied'\n  notes: retained\n")
    assert storyforge.story_source_access(story) == "denied"
    bundle = (ROOT / "tests/fixtures/mock-runs/phase5.bundle.txt").read_text().replace("{{STORY_SLUG}}", "story")
    lib.apply_artifact_bundle(story, 5, bundle, story / "runs/r")
    assert yaml.safe_load((story / "story.yaml").read_text())["source_policy"] == {
        "access": "denied", "notes": "retained"}


def test_v6_bad_replacement_final_is_checked_and_not_published(tmp_path):
    fixtures = v6_fixtures(tmp_path)
    story = tmp_path / "story"
    write(story / "source.md", "合成测试原文")
    args = ["run", "--story", story, "--runner", "mock", "--mode", "production_v6",
            "--max-retries", 0, "--no-human-gates"]
    env = {"STORYFORGE_MOCK_FIXTURE_DIR": str(fixtures)}
    assert run_storyforge(*args, "--run-id", "first", env=env).returncode == 0
    before = tree_bytes(story)
    files = lib.parse_artifact_bundle((fixtures / "phase8.bundle.txt").read_text())
    files["final.md"] = files["final.md"].replace("闻夏", "张三")
    write_bundle(fixtures / "phase8.bundle.txt", files)
    result = run_storyforge(*args, "--run-id", "replacement", "--from-phase", 8,
                           "--rubric-threshold", 10, env=env)
    assert result.returncode == 23
    rubric = json.loads((story / "runs/replacement/phase8.rubric.log").read_text())
    assert rubric["status"] == "fail"
    assert tree_bytes(story) == before


def test_changes_during_validation_are_not_overwritten(tmp_path):
    story = tmp_path / "story"
    write(story / "draft.md", "original")
    with lib.StagedStory(story, story / "runs/r", 6) as stage:
        write(stage.path / "draft.md", "candidate")
        write(story / "draft.md", "external editor change")
        with pytest.raises(OSError, match="changed during validation"):
            stage.publish()
    assert (story / "draft.md").read_text() == "external editor change"


def test_concurrent_pipeline_writer_is_rejected(tmp_path):
    story = tmp_path / "story"
    write(story / "source.md", "source")
    with lib.story_write_lock(story):
        result = run_storyforge("run", "--story", story, "--runner", "mock")
    assert result.returncode == 23
    assert "active writer" in result.stderr
    assert not (story / "final.md").exists()


@pytest.mark.parametrize("fail", [False, True])
def test_macos_exchange_argument_mapping_and_errno(tmp_path, monkeypatch, fail):
    # Exercise Darwin dispatch in Linux without claiming a macOS filesystem test.
    import ctypes
    import errno
    import os
    import types

    story = tmp_path / "story"
    write(story / "draft.md", "old")
    native = ctypes.CDLL(None, use_errno=True).renameat2
    native.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    native.restype = ctypes.c_int
    calls = []
    def renamex_np(live, candidate, flags):
        calls.append((live, candidate, flags))
        if fail:
            ctypes.set_errno(errno.ENOTSUP)
            return -1
        return native(-100, live, -100, candidate, flags)
    with lib.StagedStory(story, story / "runs/r", 6) as stage:
        write(stage.path / "draft.md", "new")
        monkeypatch.setattr(lib.sys, "platform", "darwin")
        monkeypatch.setattr(lib.ctypes, "CDLL", lambda *a, **k: types.SimpleNamespace(renamex_np=renamex_np))
        if fail:
            with pytest.raises(OSError) as error:
                stage.publish()
            assert error.value.errno == errno.ENOTSUP
        else:
            stage.publish()
        assert calls == [(os.fsencode(story), os.fsencode(stage.path), 2)]
    assert (story / "draft.md").read_text() == ("old" if fail else "new")


@pytest.mark.parametrize("publish", [False, True])
def test_process_exit_around_exchange_retains_recoverable_trees(tmp_path, publish):
    import subprocess
    story = tmp_path / "story"
    write(story / "draft.md", "old")
    code = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from storyforge_lib import StagedStory, story_write_lock
story = Path(sys.argv[2])
with story_write_lock(story), StagedStory(story, story / "runs/r", 6) as stage:
    (stage.path / "draft.md").write_text("new")
    if sys.argv[3] == "True":
        stage.publish()
    os._exit(73)
'''
    result = subprocess.run([sys.executable, "-c", code, str(ROOT / "scripts"), str(story), str(publish)], check=False)
    assert result.returncode == 73
    retained = next(tmp_path.glob(".story.attempt-*/story"))
    assert (story / "draft.md").read_text() == ("new" if publish else "old")
    assert (retained / "draft.md").read_text() == ("old" if publish else "new")
    if publish:
        record = json.loads((retained.parent / "attempt.json").read_text())
        assert lib.story_fingerprint(story) == record["candidate_fingerprint"]
        assert lib.story_fingerprint(retained) == record["original_fingerprint"]
    with lib.story_write_lock(story):
        pass  # Process death must not strand ownership.
