#!/usr/bin/env python3
"""Generate a manual prompt pack when no automatic provider can run."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--phase", required=True, type=int)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--model", default="")
    parser.add_argument("--mode", default="v4")
    args = parser.parse_args()
    started = time.time()
    run_dir = Path(args.run_dir)
    output_bundle = run_dir / f"phase{args.phase}.model.out"
    if output_bundle.exists() and output_bundle.read_text(encoding="utf-8").strip():
        result = {
            "phase": args.phase,
            "runner": "manual-prompt-pack",
            "provider": "manual-prompt-pack",
            "status": "success",
            "exit_code": 0,
            "model_or_command": "manual-existing-output",
            "duration_s": round(time.time() - started, 3),
            "output_bundle": str(output_bundle),
            "artifacts_written": [],
            "failure_reason": "",
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    pack_dir = run_dir / "manual-prompt-pack"
    pack_dir.mkdir(parents=True, exist_ok=True)
    target = pack_dir / f"phase{args.phase}.prompt.md"
    shutil.copy2(args.prompt, target)
    todo = pack_dir / f"phase{args.phase}.todo.md"
    todo.write_text(
        "\n".join(
            [
                f"# Manual Prompt Pack Phase {args.phase}",
                "",
                f"- Prompt: `{target}`",
                "- Run this prompt with a trusted agent or manually.",
                f"- Save the response as `{run_dir / f'phase{args.phase}.model.out'}`.",
                "- Re-run StoryForge from the same phase after the artifact bundle exists.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    result = {
        "phase": args.phase,
        "runner": "manual-prompt-pack",
        "provider": "manual-prompt-pack",
        "status": "failed",
        "exit_code": 24,
        "model_or_command": "manual",
        "duration_s": round(time.time() - started, 3),
        "output_bundle": str(output_bundle),
        "artifacts_written": [],
        "failure_reason": f"manual prompt pack generated: {target}",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 24


if __name__ == "__main__":
    sys.exit(main())
