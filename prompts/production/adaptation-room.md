# Adaptation Room Contract

你负责生成 3 套可投稿方向,并选出一套。必须输出:
- `adaptation.md`
- `adaptation-room.json`

`adaptation-room.json` 必须包含:
- `candidates`: 3 套方案,每套含 `premise`, `freshness_score`, `fidelity_score`, `tomato_score`, `logic_score`, `risks`
- `selected_candidate`: 只能填写被选中的候选 `id` 字符串,例如 `"A"`；禁止输出候选对象、候选摘要或嵌套 JSON。
- `replacement_map`: 原角色/道具/场景/机制载体到新设定的映射
- `mechanism_preservation`: 每个 M 机制的载体、审校要点、风险
- `sensitive_topic_policy`: 敏感议题的表达边界

Schema 硬要求:
- `replacement_map` 必须是非空对象,可以按 `roles/scenes/props_and_clues/mechanism_carriers` 分组。
- `mechanism_preservation` 必须是非空对象,键名建议使用机制 id,例如 `M2`、`M6`、`M3`,不要写成数组。
- `sensitive_topic_policy` 必须是非空对象。

选择规则:
- 神髓保真 < 8.5 不可选。
- 逻辑闭合 < 8.5 不可选。
- 新鲜度不足或一眼看出原故事,不可选。
- `selected_candidate` 必须能在 `candidates[*].id` 中精确匹配。
