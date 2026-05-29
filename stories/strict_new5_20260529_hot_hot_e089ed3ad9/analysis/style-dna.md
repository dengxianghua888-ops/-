# Style DNA

## opening_structure

```yaml
opening_structure: conflict_first
opening_summary_lines: null
opening_summary_logic_chain: null
hook_type: H1 倒叙冲突式
```

源文不是 `conclusion_first`。前10-15行没有冷静剧透完整逻辑链，而是直接进入海底捞母子重逢冲突：母亲施舍、主角拒绝、母亲让父亲认错，随后抛出“父亲三年前已死”的信息差。

## 快节奏锁定

**快节奏锁定：仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。**  
源文的痛感来自短句、对话、物证和即时反应，不来自作者替读者总结“我很痛苦”。

## 机器可读指标

```yaml
source_length_chars: 9263
chapters: 9
content_lines: 600
average_sentence_length_chars: 10.91
average_visual_line_length_chars: 15.44
short_line_rate_lte_16_chars: 0.613
long_line_rate_gte_40_chars: 0.012
direct_dialogue_line_rate: 0.357
bullet_comment_line_rate: 0.000
dialogue_char_ratio: 0.361
question_mark_density_per_1000_chars: 8.64
exclamation_mark_density_per_1000_chars: 6.37
golden_sentence_density_per_1000_chars: 1.08
```

## rhythm_contract

```yaml
allowed_average_visual_line_length_chars: [13, 18]
allowed_short_line_rate_lte_16_chars: [0.52, 0.70]
allowed_long_line_rate_gte_40_chars_max: 0.04
allowed_direct_dialogue_line_rate: [0.30, 0.45]
allowed_bullet_comment_line_rate: [0.00, 0.03]
allowed_dialogue_char_ratio: [0.32, 0.43]
allowed_question_mark_density_per_1000_chars: [6.5, 10.5]
allowed_exclamation_mark_density_per_1000_chars: [4.5, 8.0]
min_hooks_per_chapter: 1
min_rhetorical_questions_per_chapter: 4
min_evidence_reversals_per_chapter: 1
min_payoff_cards_full_text: 4
```

## 句式 DNA

- 主句短，平均一行约15字。
- 对话常单独成行，用来推进信息，不做闲聊。
- 高压段使用连续追问：
  - “你找过他一次吗？”
  - “你查过一次病历吗？”
  - “你去看过他的墓吗？”
- 判词句式短促：
  - “你不是不知道，你是不在乎！”
  - “不是感动。也不是原谅。只是觉得，太迟了。”
- 回忆段必须有具体物件落点：卡、病危通知书、助听器、遗像、蛋糕、白菊、病历。

## 对话功能

| 功能 | 典型句 | 工程要求 |
|---|---|---|
| 施压 | “你怎么和你爸一样倔？” | 反派开口必须暴露偏见 |
| 审判 | “你怎么有脸说这种话？” | 主角反问要短、硬、不给台阶 |
| 证据引爆 | “那张卡是空的！” | 每次情绪爆发必须带证据 |
| 迟来补偿无效 | “现在装什么补偿？” | 禁止把道歉写成和解入口 |
| 低温收束 | “这一次，我没有再回头。” | 结尾不喊爽，用动作断关系 |

## 金句模板

1. **否定二连 + 判词**
   - 模板：不是A。也不是B。只是C。
   - 原文功能：拒绝母亲挡刀洗白。

2. **反问 + 定罪**
   - 模板：你不是不知道，你是X。
   - 原文功能：把“误会”改判成“不在乎”。

3. **物件绑定死亡**
   - 模板：死在那张X上。
   - 原文功能：把抽象责任钉在物证上。

4. **金额反讽**
   - 模板：你少买一个X，Y就能活。
   - 原文功能：用消费错配制造恨点。

## 禁用风格

- 禁止长段解释母亲心理。
- 禁止“命运”“宿命”“终究血浓于水”等大词洗白。
- 禁止把证据写虚，如“她终于明白了一切”。
- 禁止用“眼中闪过复杂光芒”替代脸色、动作、沉默、查证结果。
