#!/usr/bin/env bash
# auto-phase.sh -- DEPRECATED: legacy Claude runner for a single Phase
#
# StoryForge V4.1 automation is now controlled by scripts/storyforge.py and
# provider runners under scripts/runners/. This script is kept only as a
# compatibility shim for workflows that still need the historical `claude -p`
# behavior.
#
# 用法:
#   ./scripts/auto-phase.sh --story stories/xxx --phase 1
#
# 前置:
#   · 本机安装了 Claude Code CLI (`which claude` 可见)
#   · 已登录 Claude (运行过 `claude` 一次)
#
# 调用关系:
#   pipeline.sh --story X --auto 会对每个 Phase 调用本脚本,替代 read -r 等待

set -euo pipefail

STORY=""
PHASE=""
MODEL="sonnet"   # 可被 --model 覆盖
MAX_TURNS=""     # 当前 claude CLI 支持时才透传

while [[ $# -gt 0 ]]; do
    case $1 in
        --story)    STORY="$2"; shift 2 ;;
        --phase)    PHASE="$2"; shift 2 ;;
        --model)    MODEL="$2"; shift 2 ;;
        --max-turns) MAX_TURNS="$2"; shift 2 ;;
        -h|--help)
            echo "用法: $0 --story <path> --phase <1-5> [--model sonnet|opus|haiku] [--max-turns n]"
            exit 0 ;;
        *)  echo "未知参数: $1" >&2; exit 10 ;;
    esac
done

if [[ -z "$STORY" || -z "$PHASE" ]]; then
    echo "错误: --story 和 --phase 都是必须参数" >&2
    exit 10
fi

if ! command -v claude >/dev/null 2>&1; then
    echo "错误: 未找到 claude CLI。请安装 Claude Code 或改用手工模式。" >&2
    exit 11
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# ---------- 每个 Phase 的任务描述 ----------

phase_prompt_1() {
cat <<EOF
你是 StoryForge V4 短篇仿写产线的 Phase 1 解构师(Dissector)。

必读(按顺序):
1. prompts/dissector.md (完整系统提示, V4)
2. prompts/patterns/reversal-mechanisms.md (8 大反转机制)
3. prompts/patterns/hook-types.md (4 种 Hook)
4. prompts/patterns/title-formulas.md (5 种标题公式)
5. prompts/patterns/forbidden-and-preferred.md (违禁/偏好词库)
6. templates/soul-contract-template.md / reader-engine-template.md / tension-ledger-template.md / platform-fit-template.md
7. ${STORY}/source.md (原文, 你要分析的输入)

任务:严格按 prompts/dissector.md 的 6 步流程, 对原文做工业级拆解。

必须产出以下文件(用 Write 工具):
- ${STORY}/dissection.md              (总报告, 顶部必须有 yaml 块含 genre/genre_confidence/genre_reasoning, 末尾必须有"题材与机制"小节)
- ${STORY}/analysis/beat-sheet.md     (10-15 个 Beat, 每 Beat 含 reversal_mechanism 字段, Beat 1 含 hook_strength)
- ${STORY}/analysis/style-dna.md      (6 维 + 第 7 维金句密度)
- ${STORY}/analysis/characters.md
- ${STORY}/analysis/theme.md
- ${STORY}/analysis/soul-contract.md  (V4 爆款神髓合约,最高约束)
- ${STORY}/analysis/reader-engine.md  (V4 逐 Beat 读者心理引擎)
- ${STORY}/analysis/tension-ledger.md (V4 情绪债账本)
- ${STORY}/analysis/platform-fit.md   (V4 番茄平台适配)

关键要求:
- Beat Sheet 每个 Beat 必须包含"原文摘录"(后续照镜子法则需要)
- dissection.md 末尾必须识别出 2-4 个反转机制(M1-M8), 给出承载 Beat 和关键金句
- 判定 genre 时选 6 个枚举之一: modern_reversal / ancient_BE / ancient_sweet / apocalypse_heroine / family_ethics / urban_sweet_ceo

完成后用可用的 shell 命令能力验证所有 9 个文件都已生成, 然后简短汇报 genre + 机制 + hook_type + 读者承诺。
EOF
}

phase_prompt_2() {
cat <<EOF
你是 StoryForge V4 Phase 2 改编师(Adapter)。

必读:
1. prompts/adapter.md
2. prompts/patterns/reversal-mechanisms.md
3. prompts/patterns/title-formulas.md
4. prompts/patterns/forbidden-and-preferred.md (按本案 genre 加载专属词)
5. ${STORY}/dissection.md (Phase 1 输出)
6. ${STORY}/analysis/beat-sheet.md
7. ${STORY}/analysis/style-dna.md
8. ${STORY}/analysis/characters.md
9. ${STORY}/analysis/theme.md
10. ${STORY}/analysis/soul-contract.md (V4 最高约束)
11. ${STORY}/analysis/reader-engine.md
12. ${STORY}/analysis/tension-ledger.md
13. ${STORY}/analysis/platform-fit.md
14. corpus/_index.json (跨篇 few-shot: 找同 genre+同机制的其它案例作参考)
15. templates/style-dna-{genre}.md (该题材基线)

任务:
- 产出 3 套改编方案, 每套含 reversal_preservation_check 表(V3 必填) + V4 爆款神髓评分矩阵
- 选定最佳方案后, 产出逐 Beat blueprint.md, 每 Beat 含反转机制执行要点 + 读者状态变化 + 情绪债变化 + 信息差变化 + 照镜子参考

必须产出:
- ${STORY}/adaptation.md
- ${STORY}/blueprint.md

完成后汇报选中哪个方案 + 改编的核心替换(世界观/主角/核心道具)。
EOF
}

phase_prompt_3() {
cat <<EOF
你是 StoryForge V4 Phase 3 写手(Writer)。

必读:
1. prompts/writer.md
2. prompts/patterns/reversal-mechanisms.md
3. prompts/patterns/forbidden-and-preferred.md
4. ${STORY}/blueprint.md
5. ${STORY}/analysis/style-dna.md
6. ${STORY}/analysis/beat-sheet.md (含照镜子参考的原文摘录)
7. ${STORY}/analysis/soul-contract.md
8. ${STORY}/analysis/reader-engine.md
9. ${STORY}/analysis/tension-ledger.md
10. corpus/_index.json (机制承载 Beat 可查同机制的跨篇 few-shot)
11. 若这是 Phase 4 FAIL 后返工,必须额外读取 ${STORY}/diff.md 与 ${STORY}/quality-report.json,逐条修复失败项

任务:严格按切片循环写作, **每次只写一个 Beat**, 写完自检 checklist:
- 本 Beat 开始时读者在等什么?
- 本 Beat 结束时读者多了什么情绪债或爽感释放?
- 是否精准卡在"还没完全满足"的位置?
- 是否保留 soul-contract.md 的主角姿态和反派恶感?
- 是否避免"只是剧情推进,但读者情绪没变化"的空 Beat?
- 文风与 style-dna 一致?
- 情绪与蓝图对齐?
- 字数在蓝图要求 ±20%?
- 无违禁词(全局+genre 专属)?
- 情绪峰值段已物理化?
- 机制承载 Beat 满足 reversal-mechanisms.md 对应机制的"审校验证要点"?
- 金句密度对齐 style-dna 第 7 维?
- 结尾精准卡在悬念钩子?
- 与上一 Beat 衔接自然?

所有 Beat 写完后拼接为:
- ${STORY}/draft.md

完成后汇报总字数 + 违禁词自检结果 + 金句密度估计 + V4 Beat 元数据。
EOF
}

phase_prompt_4() {
cat <<EOF
你是 StoryForge V4 Phase 4 审校师(Editor)。

必读:
1. prompts/editor.md
2. prompts/patterns/reversal-mechanisms.md (C5 机制保真度必查此)
3. prompts/patterns/forbidden-and-preferred.md (按 genre 扫描 4d 专属违禁)
4. ${STORY}/draft.md
5. ${STORY}/blueprint.md
6. ${STORY}/analysis/beat-sheet.md
7. ${STORY}/analysis/style-dna.md
8. ${STORY}/analysis/soul-contract.md
9. ${STORY}/analysis/reader-engine.md
10. ${STORY}/analysis/tension-ledger.md
11. templates/quality-report-template.json
12. ${STORY}/source.md (C3 独创性比对用)

任务: 对 V4 C0 神髓保真 + 5 Critical + 5 Important 维度逐项打分,并输出机器可验证质量门。

必须产出:
- ${STORY}/review.md (顶部必须含 yaml gate block: gate_status/critical_failures/important_failures)
- ${STORY}/quality-report.json (严格按 templates/quality-report-template.json)
- ${STORY}/diff.md (修改建议详单)

review.md 的 yaml gate block 必须与 quality-report.json 一致;pipeline.sh 只读取机器结构,不再 grep PASS。

所有 Critical 维度全部达标才能 PASS:
- C0 神髓禁改项 100% 通过,读者承诺兑现
- C1 情绪曲线 ≥85%
- C2 文风 DNA ≥85%
- C3 原文重复率 ≤5%
- C4 全局违禁=0 + genre 专属违禁=0 + 物理化 ≥80%
- C5 所有反转机制 checklist 项 100% 通过

完成后汇报总判定 + 失分维度(若 FAIL)。
EOF
}

phase_prompt_5() {
cat <<EOF
你是 StoryForge V4 Phase 5 定稿师(Finalizer & Polisher)。

必读:
1. prompts/finalizer.md
2. prompts/patterns/reversal-mechanisms.md (Step 2g 机制收尾验证)
3. prompts/patterns/forbidden-and-preferred.md (Step 2f genre 专属终扫)
4. ${STORY}/draft.md
5. ${STORY}/review.md
6. ${STORY}/diff.md
7. ${STORY}/quality-report.json
8. ${STORY}/analysis/soul-contract.md
9. ${STORY}/analysis/reader-engine.md
10. ${STORY}/analysis/tension-ledger.md
11. ${STORY}/analysis/platform-fit.md

任务按 finalizer.md 的 Step 1-7 顺序执行:
- Step 1: 按 diff.md 优先级修改
- Step 2a-2g: AI 除味终检(违禁词/物理化/金句锐度/genre 专属/机制收尾)
- Step 3: 输出 final.md
- Step 4: 撰写 craft-notes.md(含反转机制执行复盘表 + V4 神髓保真复盘 + 可复用资产)
- Step 5: 结构化更新 context/*.json (新违禁词/机制经验)
- Step 6: 生成番茄章节切分 final-chapters/_chapters-map.md
- Step 7: 生成 story.yaml 状态文件

必须产出:
- ${STORY}/final.md
- ${STORY}/craft-notes.md
- ${STORY}/tomato-submission.md
- ${STORY}/final-chapters/_chapters-map.md
- ${STORY}/story.yaml
- 按需更新 context/forbidden-words-learned.json, context/mechanism-playbook.json

完成后汇报最终字数 + 修改处数 + C5 机制保真结果 + V4 神髓保真结果。
EOF
}

# ---------- 调度 ----------

case "$PHASE" in
    1) TASK=$(phase_prompt_1); ROLE="Dissector" ;;
    2) TASK=$(phase_prompt_2); ROLE="Adapter" ;;
    3) TASK=$(phase_prompt_3); ROLE="Writer" ;;
    4) TASK=$(phase_prompt_4); ROLE="Editor" ;;
    5) TASK=$(phase_prompt_5); ROLE="Finalizer" ;;
    *)  echo "错误: --phase 必须为 1-5, 收到 $PHASE" >&2; exit 10 ;;
esac

echo "═══════════════════════════════════════"
echo "  Auto Phase $PHASE ($ROLE)"
echo "  Story: $STORY"
echo "  Model: $MODEL"
echo "═══════════════════════════════════════"

# 确保 analysis 目录存在(Phase 1 会写进去)
mkdir -p "$STORY/analysis"

# 调用 claude -p, 完全授权 Read/Write/Bash 工具, 非交互
# --add-dir 确保 claude 可以读写本项目文件
# --dangerously-skip-permissions 避免每次写文件都要确认(在已信任的本地环境)
CLAUDE_ARGS=(
    -p
    --model "$MODEL"
    --add-dir "$ROOT"
    --permission-mode bypassPermissions
    --allowedTools "Read Write Edit Glob Grep Bash"
    --output-format text
)

if [[ -n "$MAX_TURNS" ]]; then
    if claude --help 2>&1 | grep -q -- '--max-turns'; then
        CLAUDE_ARGS+=(--max-turns "$MAX_TURNS")
    else
        echo "错误: 当前 claude CLI 不支持 --max-turns,请删除该参数或升级 CLI。" >&2
        exit 12
    fi
fi

claude "${CLAUDE_ARGS[@]}" "$TASK"

EXIT_CODE=$?

echo ""
echo "═══════════════════════════════════════"
echo "  Auto Phase $PHASE 结束, 退出码=$EXIT_CODE"
echo "═══════════════════════════════════════"

exit $EXIT_CODE
