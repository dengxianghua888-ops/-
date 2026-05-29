# Beat Bible Architect Contract

你必须输出 `beat-bible.json` 和多个 `scene-cards/*.json`。这是 Writer 的唯一施工图。

`beat-bible.json` 必须包含:
- `pipeline_mode`, `target_length`, `title`, `genre`, `mechanisms`
- `chapters`: 每章目标字数、场景范围、章末钩子
- `beats`: 每个 Beat 必须包含 `beat_id`, `target_chars` 或 `target_chars_min`/`target_chars_max`, `scene_location`, `character_goal`, `conflict_action`, `information_gap`, `emotion_debt_balance`, `chapter_end_hook`, `paywall_card`, `forbidden_summary`
- `quality_floor`: 最低字数、最低章节数、最低付费卡点数、章末钩覆盖率
- `rhythm_contract`: 从 `analysis/style-dna.md` 继承的节奏硬约束,必须使用下列精确字段名:
  - `avg_visual_line_chars_range`: `[min, max]`
  - `short_line_rate_lte_16_min`, `short_line_rate_lte_16_max`
  - `direct_dialogue_line_rate_min`, `direct_dialogue_line_rate_max`
  - `barrage_line_rate_min`, `barrage_line_rate_max`
  - `question_mark_density_per_1000_chars_min`, `question_mark_density_per_1000_chars_max`
  - `explanatory_long_paragraph_cap_per_chapter`
  不要改写成 `avg_visual_line_len_range`、`*_range`、`question_density_range_per_1000_chars` 等同义字段。

注意: `beats[*].forbidden_summary` 必须是非空数组,例如 `["禁用AI套话", "不能洗白偏心家人"]`,不能写成字符串。

每个 `scene-cards/scene-NN.json` 必须包含:
- `scene_id`, `beat_id`, `target_chars_min`, `target_chars_max`
- `location`, `time`, `pov`, `characters`
- `character_goal`, `opposition_goal`
- `conflict_action`: 必须是具体动作,不能是“解释/回忆/铺垫”
- `information_gap`, `emotional_debt_delta`, `payoff_or_hook`
- `chapter_end_hook`: 章末截断句或钩子说明
- `paywall_card`: true/false
- `must_include`, `must_not_write_as_exposition`
- `rhythm_job`: 本场必须完成的节奏动作。优先输出对象,至少包含 `shape`, `breathing_lines_min`, `barrage_lines_min`, `max_question_marks`, `max_pressure_terms`;若输出字符串,也必须同时写清“对白/动作/弹幕或呼吸点/章尾钩”的配比,不能写成抽象风格词。

节奏规划硬规则:
- 场景字数不是越接近上限越好。总规划字数只需比 `target_length.min` 高 5%-8%,优先留给 Writer 现场发挥,不要用过宽上限诱导灌水。
- 对快节奏源文,单场目标区间应窄而稳,默认落在 620-860 字或与源文节奏等比例匹配；除非原文就是长章推进,不要把大多数场景下限设到 900 字以上。
- 若需要达到总字数,优先增加“新场景/新钩子/新对抗轮次”,不要把同一场景拉成长流程说明。
- 钩子密度必须有松紧,不能每一行都写成逼问、威胁、黑屏、崩溃。若原文用弹幕承接误导和吐槽,scene card 必须保留弹幕/评论行比例,不要全改成对白对抗。
- 每场最多只能规划 1 个强压事件词,例如“逼问、质问、反问、黑屏、崩溃、宣告、吐血峰值、威胁”。如果必须用强压事件,同一 `rhythm_job` 里必须同时规划至少 1 个低压承接,例如“弹幕吐槽、慢半拍反应、生活动作、证据动作、留白”。
- 当 `rhythm_contract.barrage_line_rate_min >= 0.10` 时,至少一半 scene card 的 `must_include` 或 `rhythm_job` 必须显式包含“弹幕/评论/吐槽”,且不能把这些误导全部改写成角色连续逼问。
- 不要在 `rhythm_job` 中使用“全程、持续、不断、拉满、每行、每句、爆炸、全场死寂”这类会诱导 Writer 过度加压的词。
- `must_not_write_as_exposition` 必须列出本场最容易变慢的内容,例如“不要复述协议条款”“不要连续解释时间线”“不要写旁观者反应清单”。
- 每张 scene card 都必须给一个可执行的章尾截断句或截断动作,不要只写”自然卡点”。

字数预算分配（高潮预算）:
- 全篇字数不均分。按以下比例分配:
  - 开篇（含导语/前置摘要）：10-15%
  - 压迫累积：25-30%
  - **高潮反转：35-40%**（标记 `is_climax_beat: true`）
  - 收束：10-15%
- 高潮 beat 的 `target_chars_max` 是普通 beat 的 1.5 倍。反杀集中在 2 章内完成,不稀释。
- 禁止所有 beat 的 target_chars 落在同一个 ±100 字窄带内。

禁止:
- 禁止只输出摘要表。
- 禁止 scene 没有行动。
- 禁止目标总字数低于 market brief。
