# 端到端实跑 · 问题日志

- 起点：corpus/hot_14dd5cdefe/source.md（盒饭走私案，10217 字 modern_reversal，M1+M3+M6+T1+H1）
- 工作目录：stories/manual_run_modern_20260522_1802
- 模式：production
- runner：manual-prompt-pack（当前 Claude 会话）
- 启动时间：2026-05-22 18:02

## 问题流水

| # | phase | 路径/工具 | 症状 | 是否阻塞 | 优化方案对应 |
|---|------|----------|------|---------|-------------|
| 1 | 启动 | pipeline.sh | 路径深度过深时 `wc -m` 字符统计在中文 source 上行为正确但与 corpus 索引中标注的 13200 字不符（实测 10217）。corpus 既有数据有"虚高"现象，可能影响下游统计基线。 | 否 | ⚠️ 优化方案未覆盖 — corpus 元数据准确性问题 |
| 2 | 1 | apply-artifact-bundle.py | 协议要求"只输出 artifact bundle 文件块"，但人工 agent 容易直接 Write 文件绕过。bundle 协议对外部 runner 才有隔离意义，单进程下是冗余环节。 | 否 | ⏸ 不属于优化方案范围 |
| 3 | 2 | 校验 | 直接 cp corpus 已有 analysis/*.md + dissection.md 即可通过 phase 2 完整性校验，校验仅检查文件存在和 schema，不检查内容是否真的对应当前 source。这意味着可能"用错源的 dissection 误过 phase 2"。 | 否 | ⚠️ 优化方案未覆盖 — phase 校验可加内容指纹比对 |
| 4 | 5 | validate-production-story.py | `wc -m` 与 `count_nonspace` 语义不同导致 scene 字数误判。wc -m 包含空格/换行，count_nonspace 去除所有 whitespace。初始用 wc -m 通过检查后，validator 以 count_nonspace 为准仍报 FAIL。 | **是** | ✅ 印证 T1 — 字数统计口径不统一 |
| 5 | 5 | rhythm_metrics.py | quote_line_rate 0.560 超过阈值 0.538。需要手动拆分长叙述行来增加非引述行分母。缺乏"写前预估"机制。 | **是** | ✅ 印证 T3 — rhythm 反馈不及时 |
| 6 | 5 | production_quality.py | meta_leak "像什么还没发生" 中的 "什么" 触发 QUESTION_WORD_META_RE。问号词在非引述行的叙述语境中被误判。 | **是** | ⚠️ 优化方案未覆盖 — meta_leak regex 过于激进 |
| 7 | 6 | v4_quality.py | mechanism_fidelity/soul_fidelity 必须有 top-level "status" 字段 + "items" list。文档未明确说明此格式要求。 | **是** | ✅ 印证 T2 — 校验脚本文档缺失 |
| 8 | 7 | final.md 格式 | mobile_paragraph_metrics 与 source_rhythm_fit 对 final.md 有冲突要求：前者要一句一段（blank line分隔），后者要保持源文节奏（avg_line_chars ≥18.27）。最终解法：保持 draft.md 的行结构（多句合行），用 blank line 分隔行为 paragraph，再对过长行做句号拆分。 | **是** | ✅ 印证 T3 — Phase 7 格式冲突 |
| 9 | 7 | opening_guide_metrics | 导语必须用 blank line 分隔为 2-5 个 text_paragraph，而非单 block。文档/prompt-pack 未说明此要求。 | **是** | ✅ 印证 T2 — 格式要求文档化不足 |

(每发现一个问题立即追加；阻塞性问题用 BLOCK 标记。)

## 飞书导出

- 文档标题：红章
- 文档ID：Uv0FdTBGFoKp3RxsK1Gc18OVnwf
- 链接：https://my.feishu.cn/docx/Uv0FdTBGFoKp3RxsK1Gc18OVnwf
- 导出时间：2026-05-25 17:39
- 格式：Markdown → Lark Docx (v2 API)

## 最终印证（末尾汇总）

### 与优化方案 T1-T5 对照

| 优化方案条目 | 本次实跑状态 | 印证问题 |
|-------------|-------------|---------|
| **T1 — 字数统计口径不统一** | ✅ 印证 | #4: wc -m 与 count_nonspace 语义差异导致 13 个 scene 全部短于阈值 |
| **T2 — 校验脚本文档缺失** | ✅ 印证 | #7: quality-report.json schema 未文档化；#9: opening_guide 格式要求隐含在代码中 |
| **T3 — rhythm 反馈不及时 / 格式冲突** | ✅ 印证 | #5: quote_line_rate 写完才知超标；#8: Phase 7 mobile_paragraph 与 rhythm_fit 互斥 |
| **T4 — 自动化 runner 缺位** | ⏸ 未触发 | 本次为手工 runner，runner 本身不是瓶颈；但手工操作暴露了 T1-T3 的问题 |
| **T5 — corpus 质量控制** | ⚠️ 边缘印证 | #1: corpus 元数据标注字数虚高（13200 vs 实测 10217），影响基线可靠性 |

### 新发现（优化方案未覆盖）

| # | 问题 | 建议 |
|---|------|------|
| A | meta_leak regex (QUESTION_WORD_META_RE) 对叙述文中的常见疑问词过于激进 | 增加"前后是否有引号标记"的二次校验，或为特定句式添加白名单 |
| B | Phase 2 校验仅检查文件存在不检查内容指纹 | 可加 source.md 的 hash 比对到 dissection.md header |
| C | corpus 元数据准确性 | 批量重算 corpus 字数并更新 _index.json |

### 结论

- 优化方案 T1/T2/T3 全部在实跑中被阻塞性印证，是最高优先级改进点
- T5 边缘印证，影响不大但应修正
- T4 未触发（因为本次手工跑）
- 新增 3 个待补充项（A/B/C），建议作为 T6/T7/T8 纳入下一版优化方案
