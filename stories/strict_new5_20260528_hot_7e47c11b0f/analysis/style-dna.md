# Style DNA

## Machine Metrics
```yaml
source_length_chars_est: 14200
avg_sentence_length_chars: 18.5
avg_visual_line_length_chars: 21.8
short_line_rate_lte_16_chars: 0.46
long_line_rate_gte_40_chars: 0.12
direct_dialogue_line_rate: 0.34
bullet_comment_line_rate: 0.04
dialogue_char_ratio: 0.31
question_mark_density_per_1k_chars: 3.1
exclamation_mark_density_per_1k_chars: 1.8
aphorism_density_per_1k_chars: 0.7
opening_structure: conflict_first
opening_summary_lines: 0
fast_pace_locked: true
```

## Opening Structure
- 判定：`conflict_first`，同时带 H4 空降揭露式 Hook。
- 不是 `conclusion_first`：前 10-15 行没有剧透完整逻辑链，没有提前说明男主追悔或女主离场结局。
- 不是 `dialogue_first`：第一推动力不是对白，而是女主奔赴、孕妻出现、男友入场的场景揭露。
- 开篇链条：秘密奔赴求婚 → 孕妇甜蜜炫夫 → 男友现身照顾孕妻 → 总裁身份暴露 → 女主确认被骗。

## 快节奏锁定
源文是快节奏短篇。仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。关键冲突必须落到：
- 现场动作：蹲下系鞋带、递卡、泼水、按头、拉黑、转身走。
- 物证：戒指、展示柜、小熊、空白支票、直播稿、红色感叹号、短信。
- 短对白：男主开价、顾雪柔设局、女主冷拒。

## 句法特征
- 短句为主，常用单句独立成段制造停顿。
- 情绪高点不直接喊痛，先写身体反应：愣住、眼泪落下、嗓子发不出声、浑身发抖。
- 对白承担推进功能，不闲聊。每轮对白都暴露新身份、新权力关系或新羞辱。
- 回忆段用于补债，不超过当前冲突的张力；回忆后必须回到现实打击。

## 高频节奏模板
1. 平静陈述期待。
2. 插入一个具体动作。
3. 动作暴露反常信息。
4. 女主短暂失语。
5. 对方继续说话，加深羞辱。
6. 女主用一个动作切断。

## 金句/低温句式
- “我以为我们是并肩走在一条泥泞的路上。”
- “结果人家从头到尾都坐在车里。”
- “你做这些事，感动不了我，只能感动你自己。”
- “有些路只能一个人走。”

这些句子不负责抒情泛滥，而负责在冲突后完成情绪定音。

## Rhythm Contract
```yaml
allowed_avg_visual_line_length_chars: [18, 26]
short_line_rate_lte_16_chars_range: [0.38, 0.55]
direct_dialogue_line_rate_range: [0.28, 0.42]
bullet_comment_line_rate_range: [0.02, 0.08]
question_mark_density_per_1k_chars_range: [2.0, 4.5]
exclamation_mark_density_per_1k_chars_range: [1.0, 3.0]
min_hooks_per_chapter: 2
min_rhetorical_questions_per_chapter: 1
min_evidence_reversals_per_chapter: 2
max_explanatory_paragraph_chars: 180
max_backstory_block_chars_without_present_conflict: 450
```

## 禁止漂移
- 禁止把女主写成持续吵闹型；她的强在越来越冷。
- 禁止把男主追悔写成有效救赎；他的每次补偿都要暴露控制欲。
- 禁止把顾雪柔简化成普通吃醋原配；她的压迫来自体面、规则和权势。
