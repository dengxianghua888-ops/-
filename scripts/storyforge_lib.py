#!/usr/bin/env python3
"""Shared StoryForge automation helpers."""

from __future__ import annotations

import fnmatch
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


V4_PHASE_KEYS = {
    1: "phase1",
    2: "phase2",
    3: "draft",
    4: "review",
    5: "final",
}
PRODUCTION_PHASE_KEYS = {
    1: "market_brief",
    2: "source_dissection",
    3: "adaptation_room",
    4: "beat_bible",
    5: "scene_writer",
    6: "critic_gauntlet",
    7: "final_packager",
    8: "feedback_learning",
}
PRODUCTION_V6_PHASE_KEYS = {
    1: "market_brief",
    2: "source_dissection_v2",
    3: "adaptation_room",
    4: "hook_writer",
    5: "beat_bible_v2",
    6: "scene_writer_v2",
    7: "critic_gauntlet",
    8: "final_packager",
    9: "feedback_learning",
}
PHASE_KEYS_BY_MODE = {
    "v4": V4_PHASE_KEYS,
    "production": PRODUCTION_PHASE_KEYS,
    "production_v6": PRODUCTION_V6_PHASE_KEYS,
    "ultra_short": PRODUCTION_PHASE_KEYS,
}


@dataclass(frozen=True)
class PhaseBundle:
    phase: int
    key: str
    role: str
    title: str
    system_prompt: str
    required_inputs: List[str]
    required_outputs: List[str]
    validators: List[str]
    human_gate: str
    retryable: bool


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now_run_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].strip()
    value = value.strip("'\"")
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in {"null", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_simple_yaml(path: Path) -> Dict[str, Any]:
    """Parse the limited YAML subset used by phase bundles and manifests."""
    data: Dict[str, Any] = {}
    current_key: str | None = None
    for raw in read_text(path).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(_parse_scalar(raw.strip()[2:]))
            continue
        if not raw.startswith((" ", "\t")) and ":" in raw:
            key, value = raw.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                data[key] = []
                current_key = key
            else:
                data[key] = _parse_scalar(value)
                current_key = None
    return data


def normalize_pipeline_mode(mode: str | None) -> str:
    value = (mode or "v4").strip().lower()
    if value in {"", "full", "fast", "v4"}:
        return "v4"
    if value in {"production", "prod"}:
        return "production"
    if value in {"production_v6", "prod_v6", "v6"}:
        return "production_v6"
    if value in {"ultra_short", "ultrashort", "short"}:
        return "ultra_short"
    raise ValueError(f"unknown pipeline mode: {mode}")


def phase_keys_for_mode(mode: str | None = None) -> Dict[int, str]:
    normalized = normalize_pipeline_mode(mode)
    return PHASE_KEYS_BY_MODE[normalized]


def phase_count(mode: str | None = None) -> int:
    return max(phase_keys_for_mode(mode))


def phase_bundle_path(phase: int, root: Path | None = None, mode: str | None = None) -> Path:
    root = root or repo_root()
    normalized = normalize_pipeline_mode(mode)
    if normalized == "production_v6":
        bundle_dir = "production-v6-phase-bundles"
    elif normalized in {"production", "ultra_short"}:
        bundle_dir = "production-phase-bundles"
    else:
        bundle_dir = "phase-bundles"
    return root / "prompts" / bundle_dir / f"phase{phase}.yaml"


def load_phase_bundle(phase: int, root: Path | None = None, mode: str | None = None) -> PhaseBundle:
    path = phase_bundle_path(phase, root, mode)
    if not path.exists():
        raise ValueError(f"missing phase bundle: {path}")
    data = parse_simple_yaml(path)
    required = ["phase", "key", "role", "title", "system_prompt", "required_outputs"]
    missing = [key for key in required if key not in data or data[key] in ("", [], None)]
    if missing:
        raise ValueError(f"{path}: missing required keys: {', '.join(missing)}")
    if int(data["phase"]) != phase:
        raise ValueError(f"{path}: phase mismatch, expected {phase}")
    outputs = list(data.get("required_outputs", []))
    if not outputs:
        raise ValueError(f"{path}: required_outputs cannot be empty")
    return PhaseBundle(
        phase=phase,
        key=str(data["key"]),
        role=str(data["role"]),
        title=str(data["title"]),
        system_prompt=str(data["system_prompt"]),
        required_inputs=list(data.get("required_inputs", [])),
        required_outputs=outputs,
        validators=list(data.get("validators", [])),
        human_gate=str(data.get("human_gate", "none")),
        retryable=bool(data.get("retryable", False)),
    )


def load_all_phase_bundles(root: Path | None = None, mode: str | None = None) -> Dict[int, PhaseBundle]:
    return {phase: load_phase_bundle(phase, root, mode) for phase in range(1, phase_count(mode) + 1)}


def validate_bundle_schema(root: Path | None = None, mode: str | None = None) -> None:
    normalized = normalize_pipeline_mode(mode)
    bundles = load_all_phase_bundles(root, normalized)
    phase_keys = phase_keys_for_mode(normalized)
    seen_outputs: set[str] = set()
    for phase, bundle in bundles.items():
        if bundle.key != phase_keys[phase]:
            raise ValueError(f"phase {phase}: key must be {phase_keys[phase]!r}")
        for rel in bundle.required_outputs:
            validate_safe_relpath(rel)
            if "*" not in rel and rel in seen_outputs:
                raise ValueError(f"artifact {rel!r} appears in more than one phase")
            if "*" not in rel:
                seen_outputs.add(rel)


def resolve_input_path(story: Path, rel: str, root: Path | None = None) -> Path:
    root = root or repo_root()
    if rel.startswith("story/"):
        return story / rel[len("story/") :]
    return root / rel


def expand_input_paths(story: Path, rel: str, root: Path | None = None) -> List[Tuple[str, Path]]:
    root = root or repo_root()
    if "*" not in rel:
        return [(rel, resolve_input_path(story, rel, root))]
    base = story if rel.startswith("story/") else root
    pattern = rel[len("story/") :] if rel.startswith("story/") else rel
    matches = sorted(path for path in base.glob(pattern) if path.is_file())
    if not matches:
        return [(rel, resolve_input_path(story, rel, root))]
    label_prefix = "story/" if rel.startswith("story/") else ""
    return [(label_prefix + str(path.relative_to(base)), path) for path in matches]


def render_phase_prompt(story: Path, phase: int, root: Path | None = None, mode: str | None = None) -> Tuple[str, Dict[str, Any]]:
    root = root or repo_root()
    normalized = normalize_pipeline_mode(mode)
    bundle = load_phase_bundle(phase, root, normalized)
    parts = [
        f"# StoryForge {normalized} Phase {phase}: {bundle.title}",
        "",
        f"Role: {bundle.role}",
        "",
        f"你正在执行 StoryForge {normalized} 自动产线。必须只输出 artifact bundle 文件块，不要直接修改文件系统。",
        "",
        "## Output Protocol",
        "",
        "每个产物必须使用以下格式：",
        "",
        "<<<FILE: relative/path.md>>>",
        "文件内容",
        "<<<END FILE>>>",
        "",
        "禁止输出绝对路径、.. 路径或未列入 required outputs 的文件。",
        "若 required outputs 包含通配符(如 scene-cards/*.json),可以输出匹配该通配符的多个文件。",
        "",
        "## Required Outputs",
        "",
    ]
    parts.extend(f"- {rel}" for rel in bundle.required_outputs)
    parts.extend(["", "## Source Materials", ""])
    manifest_inputs = []
    for rel in [bundle.system_prompt, *bundle.required_inputs]:
        for label, path in expand_input_paths(story, rel, root):
            manifest_inputs.append({"label": label, "path": str(path), "exists": path.exists()})
            parts.append(f"### {label}")
            parts.append("")
            if path.exists():
                parts.append(read_text(path))
            else:
                parts.append(f"[MISSING INPUT: {path}]")
            parts.append("")
    manifest = {
        "phase": phase,
        "role": bundle.role,
        "mode": normalized,
        "story": str(story),
        "bundle": str(phase_bundle_path(phase, root, normalized)),
        "required_outputs": bundle.required_outputs,
        "inputs": manifest_inputs,
        "rendered_at": now_stamp(),
    }
    return "\n".join(parts).rstrip() + "\n", manifest


def validate_safe_relpath(rel: str) -> Path:
    path = Path(rel)
    if path.is_absolute():
        raise ValueError(f"absolute artifact paths are not allowed: {rel}")
    if any(part == ".." for part in path.parts):
        raise ValueError(f"artifact path cannot contain '..': {rel}")
    if not str(path).strip():
        raise ValueError("artifact path cannot be empty")
    return path


def _repair_json_quotes(content: str) -> str:
    """Repair unescaped ASCII quotes inside JSON string values (common LLM issue with Chinese text)."""
    try:
        json.loads(content)
        return content
    except (json.JSONDecodeError, ValueError):
        pass
    lines = content.split('\n')
    for i, line in enumerate(lines):
        match = re.match(r'^(\s*"[^"]+"\s*:\s*)"(.+)"(\s*,?\s*)$', line)
        if match:
            prefix, value, suffix = match.group(1), match.group(2), match.group(3)
            if '"' in value:
                new_val = []
                q_open = True
                for ch in value:
                    if ch == '"':
                        new_val.append('“' if q_open else '”')
                        q_open = not q_open
                    else:
                        new_val.append(ch)
                lines[i] = f'{prefix}"{"".join(new_val)}"{suffix}'
    fixed = '\n'.join(lines)
    try:
        json.loads(fixed)
        return fixed
    except (json.JSONDecodeError, ValueError):
        return content


FILE_BLOCK_RE = re.compile(
    r"^<<<FILE:\s*(?P<path>[^>\n]+?)\s*>>>\s*\n(?P<content>.*?)\n?^<<<END FILE>>>\s*$",
    re.MULTILINE | re.DOTALL,
)

FILE_BLOCK_UNCLOSED_RE = re.compile(
    r"^<<<FILE:\s*(?P<path>[^>\n]+?)\s*>>>\s*\n(?P<content>.+)",
    re.MULTILINE | re.DOTALL,
)


def _matches_output_pattern(rel: str, pattern: str) -> bool:
    return fnmatch.fnmatchcase(rel, pattern) if "*" in pattern else rel == pattern


def _is_allowed_output(rel: str, allowed_patterns: set[str]) -> bool:
    return any(_matches_output_pattern(rel, pattern) for pattern in allowed_patterns)


def _missing_output_patterns(parsed_paths: set[str], allowed_patterns: set[str]) -> List[str]:
    missing = []
    for pattern in sorted(allowed_patterns):
        if "*" in pattern:
            if not any(_matches_output_pattern(path, pattern) for path in parsed_paths):
                missing.append(pattern)
        elif pattern not in parsed_paths:
            missing.append(pattern)
    return missing


def parse_artifact_bundle(text: str) -> Dict[str, str]:
    files: Dict[str, str] = {}
    for match in FILE_BLOCK_RE.finditer(text):
        rel = str(validate_safe_relpath(match.group("path").strip()))
        content = match.group("content")
        if not content.strip():
            raise ValueError(f"artifact block is empty: {rel}")
        files[rel] = content.rstrip() + "\n"
    if not files:
        match = FILE_BLOCK_UNCLOSED_RE.search(text)
        if match:
            rel = str(validate_safe_relpath(match.group("path").strip()))
            content = match.group("content")
            if content.strip():
                files[rel] = content.rstrip() + "\n"
    if not files:
        raise ValueError("no artifact blocks found")
    return files


def write_json(path: Path, data: Dict[str, Any]) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def apply_artifact_bundle(
    story: Path,
    phase: int,
    bundle_text: str,
    run_dir: Path,
    root: Path | None = None,
    mode: str | None = None,
) -> Dict[str, Any]:
    root = root or repo_root()
    phase_bundle = load_phase_bundle(phase, root, mode)
    allowed = set(phase_bundle.required_outputs)
    parsed = parse_artifact_bundle(bundle_text)
    # Strip "story/" prefix if model added it (common LLM output quirk)
    parsed = {k.removeprefix("story/"): v for k, v in parsed.items()}
    unknown = sorted(path for path in set(parsed) if not _is_allowed_output(path, allowed))
    if unknown and mode != "production_v6":
        raise ValueError("artifact bundle contains files not allowed for this phase: " + ", ".join(unknown))
    missing = _missing_output_patterns(set(parsed), allowed)
    if missing:
        raise ValueError("artifact bundle missing required outputs: " + ", ".join(missing))

    backup_dir = run_dir / "backups" / f"phase{phase}"
    written = []
    backed_up = []
    for rel, content in parsed.items():
        target = story / validate_safe_relpath(rel)
        if not target.resolve().is_relative_to(story.resolve()):
            raise ValueError(f"artifact path escapes story directory: {rel}")
        if target.exists():
            backup = backup_dir / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup)
            backed_up.append(rel)
        # Auto-repair JSON files with unescaped quotes (common LLM generation issue)
        if rel.endswith(".json"):
            content = _repair_json_quotes(content)
        write_text(target, content)
        written.append(rel)
    report = {
        "phase": phase,
        "status": "success",
        "written": sorted(written),
        "backed_up": sorted(backed_up),
        "required_outputs": phase_bundle.required_outputs,
        "mode": normalize_pipeline_mode(mode),
        "generated_at": now_stamp(),
    }
    write_json(run_dir / f"phase{phase}.parse-report.json", report)
    return report


def phase_range(from_phase: int) -> Iterable[int]:
    return range(from_phase, 6)


def phase_key(phase: int, mode: str | None = None) -> str:
    return phase_keys_for_mode(mode)[phase]
