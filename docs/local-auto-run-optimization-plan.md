# StoryForge V4 本地优先自动跑优化方案

## 目标

让 StoryForge V4 的 `--auto` 不依赖外部 API，也不把第三方原文发送到外部模型服务。自动跑应当在本机完成 Phase 1-5 的生成、落盘、验证、返工闭环，并保留人工校准节点。

核心原则：

- 本地原文只在本机流转，默认禁止外发。
- 生成能力与流水线编排解耦，pipeline 只关心阶段产物和质量门。
- 模型只负责“生成内容”，脚本负责“解析、写文件、验证、重试”。
- 质量门继续由确定性脚本兜底，不信任模型自评。

## 当前自动策略 Review

### 关键发现

1. `--auto` 被硬编码为 Claude Code CLI 外部执行器。
   - `pipeline.sh` 的 `run_auto_phase` 固定调用 `scripts/auto-phase.sh`。
   - `scripts/auto-phase.sh` 固定检查 `claude` CLI，并最终执行 `claude -p`。
   - 结果：网络不可用、Claude 鉴权失效、API 拒绝时，整个自动链路不可用。

2. 自动跑同时依赖“外部模型”和“模型工具执行权限”。
   - 当前任务提示要求子模型使用 `Read/Write/Edit/Grep/Bash` 直接读写项目文件。
   - 结果：模型既是创作者又是文件系统执行者，失败模式复杂，不容易做本地替换。

3. 原文版权/隐私边界没有进入自动策略。
   - corpus 和 story 的 `source.md` 是自动提示的必读输入。
   - 当前 `claude -p` 会把这些输入交给外部服务处理。
   - 结果：对“本地-only 第三方原文”无法安全自动跑。

4. Phase prompt 生成逻辑嵌在 shell 函数里，复用和测试困难。
   - 5 个 phase 的长提示全部写在 `scripts/auto-phase.sh`。
   - 结果：无法方便地给不同执行器复用同一 prompt，也难以做 prompt bundle fixture 测试。

5. 自动产物落盘缺少模型输出协议。
   - 当前依赖模型“自己写对文件”。
   - 结果：如果换成 Ollama、llama.cpp、MLX 这类本地文本生成接口，它们不会天然拥有写文件工具。

6. 自动模式跳过 Phase 2 人工确认。
   - 当前 `--auto` 直接跳过 adaptation/blueprint 的人工确认。
   - 结果：无人值守吞吐提高，但“神髓等价映射”这个高风险点容易带错进入 Phase 3。

### 结论

现有 `--auto` 本质是“Claude Code CLI 托管执行”，不是可移植的自动流水线。要实现不依赖外部 API，需要把它改造成“本地执行器 + 标准化模型输出协议 + 确定性落盘验证”的架构。

## 推荐目标架构

### 1. 增加 Runner 抽象

新增统一入口：

```bash
./pipeline.sh --story stories/x --auto --runner local
./pipeline.sh --story stories/x --auto --runner claude
./pipeline.sh --story stories/x --auto --runner mock
```

Runner 职责：

| Runner | 用途 | 是否外发 |
|--------|------|----------|
| `local` | 默认自动跑，调用本地模型服务 | 否 |
| `claude` | 显式外部模式，仅用于用户确认可外发素材 | 是 |
| `mock` | CI/回归测试，用 fixture 产物模拟模型 | 否 |
| `manual` | 保留当前人工模式 | 否 |

`pipeline.sh` 只调用：

```bash
scripts/run-phase.sh --runner "$RUNNER" --story "$STORY" --phase "$PHASE"
```

不再知道 Claude、Ollama 或具体模型命令。

### 2. 本地模型执行器

优先实现 Ollama 兼容本地 runner，因为它部署简单、HTTP 接口稳定、可完全离线。

建议默认模型分层：

| Phase | 本地模型建议 | 原因 |
|-------|--------------|------|
| Phase 1 解构 | Qwen3 / DeepSeek-R1-Distill / GLM 系中文长上下文模型 | 需要中文分析和长文抽取 |
| Phase 2 改编 | Qwen3 / Yi / GLM | 需要结构化改编与判断 |
| Phase 3 写作 | 中文创作向模型，可独立配置 | 需要文风与叙事 |
| Phase 4 审校 | 本地模型 + deterministic validators | 模型做语义判断，脚本做硬检查 |
| Phase 5 定稿 | 中文创作向模型 | 需要润色和投稿包 |

配置放入 `workspace.yaml`：

```yaml
auto:
  default_runner: local
  external_transfer_default: false
  local:
    provider: ollama
    base_url: "http://127.0.0.1:11434"
    models:
      phase1: "qwen3:32b"
      phase2: "qwen3:32b"
      phase3: "qwen3:32b"
      phase4: "qwen3:32b"
      phase5: "qwen3:32b"
    timeout_seconds: 1800
    context_policy:
      source_external_allowed: false
      max_source_chars: 60000
```

### 3. Prompt Bundle 化

把 `scripts/auto-phase.sh` 里的 shell heredoc 拆成可测试的 prompt bundle：

```text
prompts/phase-bundles/
  phase1.yaml
  phase2.yaml
  phase3.yaml
  phase4.yaml
  phase5.yaml
```

每个 bundle 声明：

```yaml
phase: 1
role: Dissector
system_prompt: prompts/dissector.md
required_inputs:
  - prompts/patterns/reversal-mechanisms.md
  - prompts/patterns/hook-types.md
  - prompts/patterns/title-formulas.md
  - prompts/patterns/forbidden-and-preferred.md
  - templates/soul-contract-template.md
  - stories/{story}/source.md
required_outputs:
  - dissection.md
  - analysis/beat-sheet.md
  - analysis/style-dna.md
  - analysis/soul-contract.md
```

新增：

```bash
scripts/render-phase-prompt.py --story stories/x --phase 1
```

它负责读取 bundle、拼接输入、记录 prompt manifest，并输出给 runner。

### 4. 标准化模型输出协议

本地模型不应该直接写文件。每个 phase 要求模型输出一个 artifact bundle：

```text
<<<FILE: dissection.md>>>
...
<<<END FILE>>>

<<<FILE: analysis/beat-sheet.md>>>
...
<<<END FILE>>>
```

然后由脚本解析并落盘：

```bash
scripts/apply-artifact-bundle.py \
  --story stories/x \
  --phase 1 \
  --bundle runs/<run-id>/phase1.model.out
```

脚本必须做：

- 只允许写入该 phase 白名单产物。
- 禁止写出 story 目录。
- 缺任何必需文件直接 fail。
- 写入前备份已有产物到 `runs/<run-id>/backups/phaseN/`。
- 写入后调用对应 validator。

这样模型换成本地 HTTP、mock fixture、未来别的本地引擎都不影响 pipeline。

### 5. Local Runner 设计

新增：

```text
scripts/run-phase.sh
scripts/runners/claude-runner.sh
scripts/runners/local-ollama-runner.py
scripts/runners/mock-runner.sh
scripts/render-phase-prompt.py
scripts/apply-artifact-bundle.py
```

`local-ollama-runner.py` 流程：

1. 读取 phase prompt。
2. 调用 `http://127.0.0.1:11434/api/generate`。
3. 将 stdout 原样保存到 `runs/<run-id>/phaseN.model.out`。
4. 调用 `apply-artifact-bundle.py` 落盘。
5. 调用 `validate-story.py` 或 `validate-quality-report.py`。
6. 返回标准退出码。

标准退出码：

| 退出码 | 含义 |
|--------|------|
| 0 | phase 成功 |
| 10 | 参数错误 |
| 11 | 缺输入 |
| 20 | 本地模型服务不可用 |
| 21 | 模型输出不可解析 |
| 22 | 缺必需产物 |
| 23 | validator fail |
| 30 | safety policy 阻止外发 |

### 6. 外发安全策略

默认策略：任何 `source.md` 默认 local-only。

每个 story 增加：

```yaml
source_policy:
  external_transfer: denied
  reason: local-only corpus source
  allowed_runners:
    - local
    - mock
    - manual
```

如果用户明确允许外部模型，必须写入 story.yaml：

```yaml
source_policy:
  external_transfer: allowed
  approved_by: human
  approved_at: "2026-04-27T23:30:00+08:00"
  allowed_runners:
    - local
    - claude
    - manual
```

`claude-runner.sh` 在读取 `source.md` 前必须检查该策略。没有明确允许就退出 `30`。

### 7. 保留人工校准，但改成显式 Gate

Phase 2 后新增可配置 gate：

```yaml
auto:
  gates:
    phase2_human_review: required_for_real_sources
```

策略：

- `mock` / 合成烟测：可跳过。
- `local` + 真实 corpus：默认暂停，等待人工确认 `adaptation.md` 与 `blueprint.md`。
- 用户可用 `--no-human-gates` 显式关闭，但要在 summary 中记录。

## 分阶段实施计划

### P0：策略与安全先落地

改动：

- `pipeline.sh` 增加 `--runner local|claude|mock|manual`，默认 `local`。
- `story.yaml` 增加 `source_policy`。
- `scripts/auto-phase.sh` 重命名或包一层为 `scripts/runners/claude-runner.sh`。
- Claude runner 默认拒绝处理 `external_transfer: denied` 的 story。

验收：

- 真实 corpus story 使用 `--runner claude` 时被本地策略阻止，而不是尝试连 API。
- 合成 story 可显式允许 `claude`。
- summary 记录 runner、provider、模型、是否外发。

### P1：Prompt Bundle 与 mock runner

改动：

- 新增 `prompts/phase-bundles/*.yaml`。
- 新增 `scripts/render-phase-prompt.py`。
- 新增 `scripts/runners/mock-runner.sh`，从 fixture 输出 artifact bundle。
- 新增 `scripts/apply-artifact-bundle.py`。

验收：

- CI 不需要任何模型即可跑通一篇 `mock` story。
- phase 必需产物缺失时 fail。
- artifact bundle 试图写 `../evil.md` 时 fail。

### P2：Ollama 本地 runner

改动：

- 新增 `scripts/runners/local-ollama-runner.py`。
- `workspace.yaml` 增加 `auto.local` 配置。
- `pipeline.sh` 的 `run_auto_phase` 改为调用统一 `run-phase.sh`。

验收：

- 关闭网络时，`--auto --runner local` 能跑到 Phase 1。
- Ollama 未启动时给出 `本地模型服务不可用`，不再提示 Claude。
- 阶段日志保存 prompt、model output、parse report、validator report。

### P3：本地生成质量加固

改动：

- 每个 phase prompt 增加 artifact bundle 输出格式要求。
- 增加 `scripts/check-artifact-completeness.py`。
- Phase 4 的机器质量报告尽量由确定性脚本生成骨架，再让模型补语义判断字段。

验收：

- 本地模型输出自然语言夹杂说明时，parser 能提取文件块。
- `quality-report.json` schema 错误时自动要求重试，不进入 Phase 5。
- Phase 4 FAIL 后仍能自动回 Phase 3，最多重试 3 次。

### P4：真实 corpus 本地试跑

改动：

- 选 3 个已人工校准样本：现代反转、家庭伦理、古言 BE。
- 使用本地 runner 跑 Phase 1-5。
- 记录每阶段生成问题、模型幻觉、格式问题、质量门失败项。

验收：

- 三篇均不触发任何外部 API。
- 每篇都有完整 `execution-summary.md`。
- 至少一篇能通过质量门进入 final。
- 未通过的样本必须有结构化失败原因。

### P5：效果闭环

改动：

- 增加 `scripts/compare-local-runs.py`，对比不同本地模型的质量报告、人工校准分、耗时。
- 增加 `runs/<run-id>/human-eval.md`。
- 把优质本地输出反哺到 `corpus/_index.json` 的成功载体字段。

验收：

- 能回答“哪个本地模型最适合 Phase 1/3/4”。
- 能从失败样本提炼 prompt 修复点。
- 自动跑不再只是跑完，而是持续逼近番茄爆款质量。

## 关键技术细节

### 本地 runner 请求格式

Ollama 请求示例：

```json
{
  "model": "qwen3:32b",
  "prompt": "<rendered phase prompt>",
  "stream": false,
  "options": {
    "temperature": 0.6,
    "num_ctx": 32768
  }
}
```

建议参数：

| Phase | temperature | top_p | 说明 |
|-------|-------------|-------|------|
| 1 | 0.2 | 0.8 | 解构要稳 |
| 2 | 0.5 | 0.9 | 改编需要发散但可控 |
| 3 | 0.75 | 0.9 | 写作需要活性 |
| 4 | 0.1 | 0.7 | 审校要严 |
| 5 | 0.55 | 0.85 | 润色适中 |

### Artifact Bundle Parser 规则

允许：

```text
<<<FILE: relative/path.md>>>
content
<<<END FILE>>>
```

拒绝：

- 绝对路径。
- 包含 `..`。
- 不在 phase 输出白名单中。
- 同一文件重复出现。
- 必需文件为空。

### 日志目录

建议每个 phase 记录：

```text
runs/<run-id>/
  phase1.prompt.md
  phase1.prompt-manifest.json
  phase1.model.out
  phase1.parse-report.json
  phase1.validator.log
  phase1.log
```

这样出问题时能分清是 prompt、模型、解析、落盘还是质量门问题。

## 风险与应对

| 风险 | 表现 | 应对 |
|------|------|------|
| 本地模型中文长文能力不稳 | Phase 1 漏 Beat、漏神髓禁改项 | Phase 1 拆成 source chunk + synthesis 两步 |
| 本地模型格式服从差 | artifact bundle 不完整 | parser fail 后自动追加“只修格式”重试 |
| 写作质量低于外部强模型 | Phase 3 情绪和文风弱 | 强化 few-shot、人工校准样本、分 Beat 生成 |
| 本地硬件跑不动大模型 | 超时或上下文不足 | 支持小模型 + 分块；Phase 3 按 Beat 调用 |
| 自动跑又变成低质吞吐 | 跳过人工判断 | 真实来源默认保留 Phase 2 人工 gate |

## 推荐下一步

1. 先做 P0 + P1：把安全策略、runner 抽象、prompt bundle、mock runner 打通。
2. 再做 P2：接 Ollama 本地 runner。
3. 用合成 story 跑 mock 回归，再用本地模型跑 `v4_smoke_local_rules`。
4. 最后挑 1 篇已人工校准 corpus 做真实本地试跑，不触发外部 API。

这条路线的重点不是马上换一个模型命令，而是把自动产线从“外部 Agent 帮我操作仓库”改成“本地流水线驱动模型生成、脚本负责可靠落盘与验证”。这样后续无论用 Ollama、MLX、llama.cpp，还是未来换成本地微调模型，产线骨架都不需要再重写。
