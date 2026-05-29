# 五篇产线持续生产稳定性测试报告

测试时间：2026-05-09  
执行方式：`codex runner`，五篇依次执行，失败后按阶段 validator 定位并修复。  
最终结论：5/5 篇完成 Phase 8 强校验，全部通过；5 篇正文已导出飞书。

## 产出清单

| 序号 | 本地目录 | 最终字数 | 章节 | 钩子覆盖 | 付费卡点 | 飞书正文 |
|---|---|---:|---:|---:|---:|---|
| 1 | `stories/prod_batch_01_autopsy_vow` | 11760 | 16 | 100% | 8 | https://my.feishu.cn/docx/TkbIdkVQAovEGvxycdDcDULOnPz |
| 2 | `stories/prod_batch_02_abyss_profile` | 12716 | 16 | 100% | 10 | https://my.feishu.cn/docx/S0vjdnQTGo3WYoxuYx5cCVZ7nMT |
| 3 | `stories/prod_batch_03_empress_exit` | 14259 | 15 | 100% | 16 | https://my.feishu.cn/docx/YNgmda3WOo9875xhatfcPqb8nch |
| 4 | `stories/prod_batch_04_blossom_network` | 11427 | 16 | 100% | 8 | https://my.feishu.cn/docx/VTPqd5r8eopnovxekBCcgxGNnis |
| 5 | `stories/prod_batch_05_allowance_truth` | 12895 | 16 | 100% | 10 | https://my.feishu.cn/docx/IBCqdl1dNotuHOxkklJcyQZjnWf |

## 通过项

- 五篇均通过 `validate-production-story.py --phase 8 --mode production --require-pass --json`。
- 最终稿均满足目标字数、章节长度、章节钩子覆盖、付费卡点、源文连续重合、重复片段、硬禁词和软禁词门槛。
- 第 5 篇在 Phase 7 重新按 16 个场景拆章后，章节长度全部落回 500-1200 范围。

## 稳定性问题

- runner 长阶段缺少中间心跳，Phase 2/5/7 会出现数分钟静默，只能通过 run 目录和 validator 观察。
- Phase 3 偶发 `adaptation-room.json selected_candidate` 输出对象而非字符串 id。
- Phase 4 稳定复现 `beat-bible.json beats[*].forbidden_summary` 输出字符串，validator 要求非空数组。
- Phase 5 容易出现场景字数越界和软禁词残留，常见词为“轻轻/淡淡/微微”。
- Phase 6 稳定复现评分尺度 0-100 与 validator 0-10 不一致，`review.md` 缺机器可读 YAML gate，`quality-report.json machine_metrics` 经常幻觉或滞后。
- Phase 7 经常产物已写出但因 `quality-report.json` 最终指标未刷新、`story.yaml status` 未设为 `final` 而失败。
- 第 4 篇 Phase 7 出现一次外层会话长时间无输出，真实进程后续写完并以 validator 失败退出；可观测性不足。
- 第 5 篇 Phase 7 packager 将 16 场压成 12 章，导致部分章节超过 1200 字，需要按场景重拆。

## 建议

- 在 runner 调用外层增加阶段心跳和当前 provider/PID 输出。
- 在 Phase 3/4 写入后增加 schema-normalizer，提前处理对象/id、字符串/数组这类机械错误。
- 在 Phase 6 输出前强制评分归一、写 YAML gate，并用真实 `machine_evaluate` 回填 `machine_metrics`。
- 在 Phase 7 packager 增加章节长度硬约束，优先保持 scene-card 拆分，不要合并到超长章节。
