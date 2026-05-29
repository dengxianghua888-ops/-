#!/usr/bin/env python3
"""Shared StoryForge V4 validation helpers."""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


GLOBAL_FORBIDDEN = [
    "然而",
    "总而言之",
    "不禁",
    "心中涌起",
    "深吸一口气",
    "宛如命运的齿轮",
    "眼中闪过一丝",
    "嘴角微微上扬",
    "不由得",
    "颤抖着说道",
    "空气仿佛凝固",
]

SOFT_FORBIDDEN = ["悄然", "缓缓", "默默", "微微", "淡淡", "轻轻"]
FORBIDDEN_EXCEPTIONS = {
    "然而": ["戛然而止"],
}

PHYSICAL_EMOTION_MARKERS = [
    "耳鸣",
    "指尖",
    "发麻",
    "后槽牙",
    "太阳穴",
    "青筋",
    "手心",
    "后背",
    "冷汗",
    "胸腔",
    "喉咙",
    "眼眶",
    "头皮",
    "心脏",
    "指甲",
    "掌心",
]

VALID_GATE_STATUS = {"pass", "fail"}
VALID_STORY_STATUSES = {"phase1", "phase2", "draft", "review_failed", "final", "submitted"}
CALIBRATION_GENE_FIELDS = (
    "reader_promise",
    "emotional_debt_type",
    "dominant_s爽点",
    "antagonist_violation",
    "protagonist_stance",
    "payoff_pattern",
    "tomato_fit_score",
)
PHASE_ALIASES = {
    "1": "phase1",
    "phase1": "phase1",
    "2": "phase2",
    "phase2": "phase2",
    "3": "draft",
    "phase3": "draft",
    "draft": "draft",
    "4": "review",
    "phase4": "review",
    "review": "review",
    "5": "final",
    "phase5": "final",
    "final": "final",
}

PHASE_ARTIFACTS = {
    "phase1": [
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
    ],
    "phase2": ["adaptation.md", "blueprint.md"],
    "draft": ["draft.md"],
    "review": ["review.md", "quality-report.json", "diff.md"],
    "final": [
        "final.md",
        "craft-notes.md",
        "tomato-submission.md",
        "final-chapters/_chapters-map.md",
        "story.yaml",
    ],
}
PHASE_ORDER = ["phase1", "phase2", "draft", "review", "final"]


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}")


def _parse_inline_list(value: str) -> List[str]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip("'\"") for item in inner.split(",")]


def _extract_yaml_block_list(section: str, key: str) -> List[str]:
    lines = section.splitlines()
    for index, raw in enumerate(lines):
        stripped = raw.strip()
        if not stripped.startswith(f"{key}:"):
            continue
        value = stripped.split(":", 1)[1].strip()
        if value.startswith("[") and value.endswith("]"):
            return _parse_inline_list(value)
        items = []
        base_indent = len(raw) - len(raw.lstrip(" "))
        for child in lines[index + 1:]:
            child_stripped = child.strip()
            child_indent = len(child) - len(child.lstrip(" "))
            if not child_stripped:
                continue
            if child_indent <= base_indent and not child_stripped.startswith("- "):
                break
            if child_stripped.startswith("- "):
                items.append(child_stripped[2:].strip().strip("'\""))
        return items
    return []


def _extract_top_section(text: str, key: str) -> str:
    pattern = rf"^{re.escape(key)}:\s*\n(.*?)(?=^\S|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def _extract_genre_section(text: str, genre: str) -> str:
    genre_profiles = _extract_top_section(text, "genre_profiles")
    pattern = rf"^  {re.escape(genre)}:\s*\n(.*?)(?=^  [A-Za-z0-9_]+:\s*$|\Z)"
    match = re.search(pattern, genre_profiles, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def _extract_scalar_int(section: str, key: str, default: int) -> int:
    match = re.search(rf"^\s*{re.escape(key)}:\s*([0-9]+)", section, re.MULTILINE)
    return int(match.group(1)) if match else default


def find_workspace_yaml(start: Path) -> Path | None:
    start = start.resolve()
    base = start if start.is_dir() else start.parent
    for path in [base, *base.parents]:
        candidate = path / "workspace.yaml"
        if candidate.exists():
            return candidate
    candidate = Path.cwd() / "workspace.yaml"
    return candidate if candidate.exists() else None


def load_workspace_policy(start: Path | None = None) -> Dict[str, Any]:
    policy = {
        "forbidden_words": list(GLOBAL_FORBIDDEN),
        "soft_forbidden": list(SOFT_FORBIDDEN),
        "soft_forbidden_max": 2,
        "title_max_chars": 30,
        "genre_extra_forbidden": {},
    }
    workspace = find_workspace_yaml(start or Path.cwd())
    if not workspace:
        return policy
    text = workspace.read_text(encoding="utf-8")
    ai_flavor = _extract_top_section(text, "ai_flavor")
    tomato = _extract_top_section(text, "tomato")
    forbidden = _extract_yaml_block_list(ai_flavor, "forbidden_words")
    soft = _extract_yaml_block_list(ai_flavor, "soft_forbidden")
    if forbidden:
        policy["forbidden_words"] = forbidden
    if soft:
        policy["soft_forbidden"] = soft
    policy["title_max_chars"] = _extract_scalar_int(tomato, "title_max_chars", policy["title_max_chars"])

    genre_extras = {}
    for match in re.finditer(r"^  ([A-Za-z0-9_]+):\s*$", _extract_top_section(text, "genre_profiles"), re.MULTILINE):
        genre = match.group(1)
        extras = _extract_yaml_block_list(_extract_genre_section(text, genre), "extra_forbidden")
        if extras:
            genre_extras[genre] = extras
    policy["genre_extra_forbidden"] = genre_extras
    return policy


def parse_simple_yaml_block(text: str) -> Dict[str, Any]:
    """Parse the small review gate block without requiring PyYAML."""
    block = None
    fenced = re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        block = fenced.group(1)
    else:
        head = "\n".join(text.splitlines()[:12])
        if "gate_status:" in head:
            block = head

    if block is None:
        raise ValueError("missing machine-readable gate block in review.md")

    data: Dict[str, Any] = {}
    current_list_key = None
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- ") and current_list_key:
            data.setdefault(current_list_key, []).append(line[2:].strip().strip("'\""))
            continue
        if ":" not in line:
            current_list_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in ("[]", ""):
            data[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [] if not inner else [x.strip().strip("'\"") for x in inner.split(",")]
            current_list_key = key
        else:
            data[key] = value.strip("'\"")
            current_list_key = None

    if "gate_status" not in data:
        raise ValueError("missing gate_status in machine-readable gate block")
    return data


def load_review_gate(story: Path) -> Dict[str, Any]:
    review = story / "review.md"
    if not review.exists():
        raise ValueError(f"missing file: {review}")
    gate = parse_simple_yaml_block(review.read_text(encoding="utf-8"))
    normalize_gate(gate, source="review.md")
    return gate


def normalize_gate(data: Dict[str, Any], source: str) -> None:
    status = str(data.get("gate_status", "")).lower()
    if status not in VALID_GATE_STATUS:
        raise ValueError(f"{source}: gate_status must be pass or fail")
    data["gate_status"] = status
    for key in ("critical_failures", "important_failures"):
        value = data.get(key, [])
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError(f"{source}: {key} must be a list")
        data[key] = value
    if status == "pass" and data["critical_failures"]:
        raise ValueError(f"{source}: pass gate cannot contain critical_failures")


def _validate_status(value: Any, source: str) -> str:
    status = str(value).lower()
    if status not in VALID_GATE_STATUS:
        raise ValueError(f"{source}: status must be pass or fail")
    return status


def _collect_hard_check_failures(hard_checks: Dict[str, Any]) -> List[str]:
    failures = []
    for key, value in hard_checks.items():
        if isinstance(value, str):
            status = _validate_status(value, f"quality-report.json: hard_checks.{key}")
        elif isinstance(value, dict):
            if "status" not in value:
                raise ValueError(f"quality-report.json: hard_checks.{key}.status is required")
            status = _validate_status(value["status"], f"quality-report.json: hard_checks.{key}")
            if key == "forbidden_words" and value.get("hits") and status == "pass":
                raise ValueError(f"quality-report.json: hard_checks.{key} has hits but status=pass")
        else:
            raise ValueError(f"quality-report.json: hard_checks.{key} must be a string or object")
        if status == "fail":
            failures.append(f"hard_checks.{key}")
    return failures


def _collect_fidelity_failures(report: Dict[str, Any], key: str) -> List[str]:
    section = report.get(key)
    if not isinstance(section, dict):
        raise ValueError(f"quality-report.json: {key} must be an object")
    if "status" not in section:
        raise ValueError(f"quality-report.json: {key}.status is required")
    failures = []
    section_status = _validate_status(section["status"], f"quality-report.json: {key}")
    if section_status == "fail":
        failures.append(key)
    items = section.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"quality-report.json: {key}.items must be a list")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"quality-report.json: {key}.items[{index}] must be an object")
        if "status" not in item:
            raise ValueError(f"quality-report.json: {key}.items[{index}].status is required")
        item_status = _validate_status(item["status"], f"quality-report.json: {key}.items[{index}]")
        if item_status == "fail":
            failures.append(f"{key}.items[{index}]")
    return failures


def validate_quality_report_contract(report: Dict[str, Any]) -> None:
    hard_checks = report.get("hard_checks")
    if not isinstance(hard_checks, dict):
        raise ValueError("quality-report.json: hard_checks must be an object")
    failures = []
    failures.extend(_collect_hard_check_failures(hard_checks))
    failures.extend(_collect_fidelity_failures(report, "mechanism_fidelity"))
    failures.extend(_collect_fidelity_failures(report, "soul_fidelity"))

    if report["gate_status"] == "pass" and failures:
        raise ValueError(
            "quality-report.json: pass gate has failing critical checks: "
            + ", ".join(failures)
        )
    if report["gate_status"] == "fail" and failures and not report["critical_failures"]:
        raise ValueError("quality-report.json: failing critical checks require critical_failures")


def load_quality_report(story: Path) -> Dict[str, Any]:
    report = load_json(story / "quality-report.json")
    normalize_gate(report, source="quality-report.json")
    for key in ("hard_checks", "mechanism_fidelity", "soul_fidelity"):
        if key not in report:
            raise ValueError(f"quality-report.json: missing {key}")
    validate_quality_report_contract(report)
    return report


def validate_quality_report(story: Path) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    review_gate = load_review_gate(story)
    report = load_quality_report(story)
    if review_gate["gate_status"] != report["gate_status"]:
        raise ValueError("review.md gate_status does not match quality-report.json")
    if review_gate["critical_failures"] != report["critical_failures"]:
        raise ValueError("review.md critical_failures does not match quality-report.json")
    if review_gate["important_failures"] != report["important_failures"]:
        raise ValueError("review.md important_failures does not match quality-report.json")
    return review_gate, report


def parse_metadata_block(text: str, source: str = "metadata") -> Dict[str, Any]:
    fenced = re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    if not fenced:
        raise ValueError(f"missing yaml metadata block in {source}")
    data = {}
    for raw in fenced.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_simple_yaml_value(value)
    return data


def parse_human_calibration_fields(text: str) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}
    for key in CALIBRATION_GENE_FIELDS:
        pattern = rf"^{re.escape(key)}:\s*(.+)$"
        match = re.search(pattern, text, re.MULTILINE)
        if not match:
            continue
        value = match.group(1).strip()
        if key == "tomato_fit_score":
            try:
                fields[key] = float(value)
            except ValueError:
                fields[key] = value
        else:
            fields[key] = value
    return fields


def load_human_calibration(slug_dir: Path, require_approved: bool = False) -> Dict[str, Any]:
    path = slug_dir / "analysis" / "human-calibration.md"
    if not path.exists():
        if require_approved:
            raise ValueError(f"missing human calibration file: {path}")
        return {}
    text = path.read_text(encoding="utf-8")
    gate = parse_metadata_block(text, source="human calibration")
    decision = str(gate.get("decision", "")).strip()
    if decision != "approved":
        if require_approved:
            raise ValueError("human calibration decision must be approved")
        return {}
    reviewer = str(gate.get("reviewer", "")).strip()
    reviewed_at = str(gate.get("reviewed_at", "")).strip()
    if not reviewer or not reviewed_at:
        raise ValueError("approved human calibration requires reviewer and reviewed_at")
    if re.search(r"^- \[ \]", text, re.MULTILINE):
        raise ValueError("unchecked checklist items remain in human calibration")
    fields = parse_human_calibration_fields(text)
    missing = [key for key in CALIBRATION_GENE_FIELDS if key not in fields or fields[key] in ("", None)]
    if missing:
        raise ValueError("approved human calibration missing fields: " + ", ".join(missing))
    fields.update({
        "v4_human_reviewer": reviewer,
        "v4_human_reviewed_at": reviewed_at,
    })
    return fields


def normalize_phase(phase: str) -> str:
    normalized = PHASE_ALIASES.get(str(phase).lower())
    if not normalized:
        valid = ", ".join(sorted(PHASE_ALIASES))
        raise ValueError(f"unknown phase {phase!r}; expected one of: {valid}")
    return normalized


def _strip_yaml_comment(value: str) -> str:
    if " #" in value:
        value = value.split(" #", 1)[0]
    return value.strip()


def parse_simple_yaml_value(value: str) -> Any:
    value = _strip_yaml_comment(value).strip().strip("'\"")
    if value == "":
        return ""
    if value in {"[]", "[ ]"}:
        return []
    if value.lower() in {"null", "~"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [x.strip().strip("'\"") for x in inner.split(",")]
    return value


def load_story_manifest(story: Path) -> Dict[str, Any]:
    """Parse the small story.yaml status manifest without a PyYAML dependency."""
    path = story / "story.yaml"
    if not path.exists():
        raise ValueError(f"missing file: {path}")

    manifest: Dict[str, Any] = {}
    current_section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith((" ", "\t")) and ":" in raw:
            key, value = raw.split(":", 1)
            key = key.strip()
            parsed = parse_simple_yaml_value(value)
            if parsed == "":
                manifest[key] = {}
                current_section = key
            else:
                manifest[key] = parsed
                current_section = None
        elif current_section and raw.startswith("  ") and ":" in raw:
            key, value = raw.split(":", 1)
            section = manifest.setdefault(current_section, {})
            if isinstance(section, dict):
                section[key.strip()] = parse_simple_yaml_value(value)
    return manifest


def count_nonspace(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def count_term(text: str, term: str) -> int:
    count = text.count(term)
    for exception in FORBIDDEN_EXCEPTIONS.get(term, []):
        count -= text.count(exception)
    return max(count, 0)


def count_hits(text: str, terms: Iterable[str]) -> Dict[str, int]:
    hits = {}
    for term in terms:
        count = count_term(text, term)
        if count:
            hits[term] = count
    return hits


def sentence_lengths(text: str) -> List[int]:
    parts = re.split(r"[。！？!?；;]\s*", text)
    return [count_nonspace(part) for part in parts if count_nonspace(part) > 0]


def dialogue_chars(text: str) -> int:
    total = 0
    for match in re.finditer(r"[“\"]([^”\"]+)[”\"]", text):
        total += count_nonspace(match.group(1))
    return total


def style_metrics(text: str) -> Dict[str, Any]:
    chars = count_nonspace(text)
    lengths = sentence_lengths(text)
    avg_sentence_length = round(sum(lengths) / len(lengths), 3) if lengths else 0
    dchars = dialogue_chars(text)
    per_k_base = chars / 1000 if chars else 1
    return {
        "char_count": chars,
        "sentence_count": len(lengths),
        "avg_sentence_length": avg_sentence_length,
        "dialogue_ratio": round(dchars / chars, 4) if chars else 0,
        "question_marks": text.count("？") + text.count("?"),
        "question_marks_per_k": round((text.count("？") + text.count("?")) / per_k_base, 3),
        "physical_emotion_hits": count_hits(text, PHYSICAL_EMOTION_MARKERS),
        "forbidden_hits": count_hits(text, GLOBAL_FORBIDDEN),
        "soft_forbidden_hits": count_hits(text, SOFT_FORBIDDEN),
    }


def normalize_ratio_value(value: Any) -> Any:
    if isinstance(value, (int, float)) and value > 1:
        return round(float(value) / 100.0, 6)
    return value


def stats(values: List[float]) -> Dict[str, Any]:
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return {"mean": None, "std": None, "n": 0, "samples": []}
    mean = sum(clean) / len(clean)
    std = 0.0
    if len(clean) > 1:
        std = math.sqrt(sum((v - mean) ** 2 for v in clean) / (len(clean) - 1))
    return {
        "mean": round(mean, 3),
        "std": round(std, 3),
        "n": len(clean),
        "samples": [round(v, 6) for v in clean],
    }


def required_artifacts_for_phase(phase: str) -> List[str]:
    phase = normalize_phase(phase)
    artifacts: List[str] = []
    for current in PHASE_ORDER:
        artifacts.extend(PHASE_ARTIFACTS[current])
        if current == phase:
            break
    return artifacts


def missing_artifacts(story: Path, phase: str) -> List[str]:
    return [rel for rel in required_artifacts_for_phase(phase) if not (story / rel).exists()]
