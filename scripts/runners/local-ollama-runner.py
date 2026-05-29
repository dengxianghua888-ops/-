#!/usr/bin/env python3
"""Optional Ollama runner for local-only StoryForge generation."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", required=True)
    parser.add_argument("--phase", required=True, type=int)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--model", default="qwen3:32b")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    args = parser.parse_args()

    started = time.time()
    run_dir = Path(args.run_dir)
    output = run_dir / f"phase{args.phase}.model.out"
    prompt = Path(args.prompt).read_text(encoding="utf-8")
    payload = json.dumps(
        {
            "model": args.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.6, "num_ctx": 32768},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        args.base_url.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=1800) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        result = {
            "phase": args.phase,
            "runner": "local-ollama",
            "provider": "ollama",
            "status": "failed",
            "exit_code": 20,
            "model_or_command": args.model,
            "duration_s": round(time.time() - started, 3),
            "output_bundle": str(output),
            "artifacts_written": [],
            "failure_reason": f"ollama unavailable or invalid response: {exc}",
        }
        print(json.dumps(result, ensure_ascii=False))
        return 20

    output.write_text(str(data.get("response", "")), encoding="utf-8")
    result = {
        "phase": args.phase,
        "runner": "local-ollama",
        "provider": "ollama",
        "status": "success",
        "exit_code": 0,
        "model_or_command": args.model,
        "duration_s": round(time.time() - started, 3),
        "output_bundle": str(output),
        "artifacts_written": [],
        "failure_reason": "",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
