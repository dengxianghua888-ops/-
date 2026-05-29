# Source Dissector Contract

你要把原文拆成可执行的爆款工程数据。必须输出:
- `story-brief.json`
- `dissection.md`
- `analysis/beat-sheet.md`
- `analysis/style-dna.md`
- `analysis/soul-contract.md`
- `analysis/reader-engine.md`
- `analysis/tension-ledger.md`

`story-brief.json` 必须包含:
- `source_title`, `genre`, `hook_type`, `title_formula`
- `reversal_mechanisms`
- `source_length_chars`
- `reader_promise`
- `emotional_debts`
- `payoff_pattern`
- `forbidden_to_change`
- `replaceable_assets`

Schema 硬要求:
- `hook_type` 必须是非空字符串,不要写成对象。
- `title_formula` 必须是非空字符串,不要写成对象。
- `payoff_pattern` 必须是非空字符串,可以用分号串联关键节奏,不要写成数组。
- `reversal_mechanisms`, `emotional_debts`, `forbidden_to_change`, `replaceable_assets` 必须是数组。

拆解要求:
- Beat 必须精确到原文段落/句子证据。
- 每个 Beat 必须有情绪强度、信息差、读者期待、章尾钩功能。
- Style DNA 必须给机器可读数值: 平均句长、平均可视行长、短行率(<=16字行占比)、长行率(>=40字行占比)、直接对白行率、弹幕/评论行率、对话占比、问号密度、感叹号密度、金句密度。
- Style DNA 必须写出 `rhythm_contract`: 终稿允许的平均可视行长区间、短行率上下限、直接对白行率上下限、弹幕/评论行率上下限、问号密度上下限、单章内最少钩子/反问/证据翻转次数。
- 若原文是快节奏短篇,必须标注”快节奏锁定”: 仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。
- 禁止只概括剧情。

开篇结构分析（必填,写入 `analysis/style-dna.md`）:
- 判断源文属于哪种开篇结构:
  - `conclusion_first`: 前 10-15 行冷静剧透完整故事逻辑链（约 28% 番茄爆款使用）
  - `conflict_first`: 直接进入冲突场景
  - `dialogue_first`: 以对白开篇
- 标注字段 `opening_structure` 到 style-dna.md
- 若为 `conclusion_first`,同时标注 `opening_summary_lines`（摘要行数）和前置摘要覆盖的逻辑链要素（极端处境 + 荒谬行为 + 反击方式 + payoff 预告）
