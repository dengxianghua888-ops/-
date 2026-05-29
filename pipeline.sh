#!/usr/bin/env bash
# pipeline.sh -- StoryForge V4 compatibility wrapper.
#
# The automation state machine lives in scripts/storyforge.py. This wrapper keeps
# the historical CLI shape while routing execution through the Python controller.

set -euo pipefail

STORY=""
FROM_PHASE=1
RUN_ID=""
MAX_RETRIES=3
RUNNER="manual-prompt-pack"
MODEL=""
DRY_RUN=false
NO_HUMAN_GATES=false
MODE="v4"

ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --story) STORY="$2"; shift 2 ;;
        --phase|--from-phase) FROM_PHASE="$2"; shift 2 ;;
        --run-id) RUN_ID="$2"; shift 2 ;;
        --max-retries) MAX_RETRIES="$2"; shift 2 ;;
        --runner) RUNNER="$2"; shift 2 ;;
        --auto) RUNNER="agent"; shift ;;
        --auto-model|--model) MODEL="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        --no-human-gates) NO_HUMAN_GATES=true; shift ;;
        --mode) MODE="$2"; shift 2 ;;
        -h|--help)
            cat <<'EOF'
用法:
  ./pipeline.sh --story <path> [--phase 1-5] [--dry-run]
  ./pipeline.sh --story <path> --mode production --auto [--runner agent|codex|openclaw|claude|mock|local-ollama]
  ./pipeline.sh --story <path> --mode ultra_short --auto [--runner agent|codex|openclaw|claude|mock|local-ollama]
  ./pipeline.sh --story <path> --auto [--runner agent|codex|openclaw|claude|mock|local-ollama]
  ./pipeline.sh --story <path> --runner mock --no-human-gates

说明:
  pipeline.sh 现在是兼容 wrapper，真实主控为:
  python3 scripts/storyforge.py run --story <path> --runner <runner> --mode <v4|production|ultra_short>

常用 runner:
  agent              Codex -> OpenClaw -> Claude -> manual-prompt-pack fallback
  mock               离线 fixture runner，用于回归测试
  manual-prompt-pack 只生成 prompt 包，供人工或外部 agent 接力
  local-ollama       显式启用本地 Ollama，不作为默认路径
EOF
            exit 0 ;;
        *)
            ARGS+=("$1"); shift ;;
    esac
done

if [[ -z "$STORY" ]]; then
    echo "错误: --story 为必须参数" >&2
    exit 10
fi

CMD=(python3 scripts/storyforge.py run --story "$STORY" --from-phase "$FROM_PHASE" --runner "$RUNNER" --max-retries "$MAX_RETRIES" --mode "$MODE")
if [[ -n "$RUN_ID" ]]; then
    CMD+=(--run-id "$RUN_ID")
fi
if [[ -n "$MODEL" ]]; then
    CMD+=(--model "$MODEL")
fi
if $DRY_RUN; then
    CMD+=(--dry-run)
fi
if $NO_HUMAN_GATES; then
    CMD+=(--no-human-gates)
fi
if [[ ${#ARGS[@]} -gt 0 ]]; then
    CMD+=("${ARGS[@]}")
fi

exec "${CMD[@]}"
