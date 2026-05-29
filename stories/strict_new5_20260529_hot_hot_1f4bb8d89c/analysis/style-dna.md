# Style DNA

## Machine Metrics

```yaml
source_length_chars: 12680
avg_sentence_length_chars: 17.8
avg_visible_line_length_chars: 18.6
short_line_rate_lte_16_chars: 0.54
long_line_rate_gte_40_chars: 0.05
direct_dialogue_line_rate: 0.43
barrage_or_comment_line_rate: 0.00
dialogue_char_ratio: 0.41
question_mark_density_per_1000_chars: 4.4
exclamation_mark_density_per_1000_chars: 0.8
golden_sentence_density_per_1000_chars: 1.5
opening_structure: conflict_first
fast_pace_lock: true
```

## Opening Structure

源文开篇结构是 `conflict_first`。

不是 `conclusion_first`，因为前10-15行没有冷静剧透完整逻辑链，而是直接进入婚礼冲突现场：棺材礼、全场死寂、女主淡笑、反手文件。

也不是纯 `dialogue_first`，因为第一句是动作事件：“婚礼当天，傅沉舟让人送来一顶棺材。” 对白随后进入，用来放大羞辱。

## 快节奏锁定

源文属于快节奏短篇。仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。

必须保留：

- 现场冲突先行：婚礼、酒吧、咖啡馆、上门挽回都以对话和动作推进。
- 短句砸点：关键断情句必须短。
- 证据翻转：合同、体检报告、婚戒、星星罐、重生秘密都要成为剧情推进物。
- 情绪不靠哭诉：女主大部分时候“淡淡一笑”“冷冷开口”“没有回头”。

## Rhythm Contract

```yaml
allowed_avg_visible_line_length_chars:
  min: 16
  max: 22
short_line_rate_lte_16_chars:
  min: 0.45
  max: 0.62
direct_dialogue_line_rate:
  min: 0.35
  max: 0.50
barrage_or_comment_line_rate:
  min: 0.00
  max: 0.03
question_mark_density_per_1000_chars:
  min: 3.2
  max: 5.8
exclamation_mark_density_per_1000_chars:
  min: 0.3
  max: 1.5
min_hooks_per_chapter: 1
min_rhetorical_questions_per_chapter: 1
min_evidence_reversals_per_chapter: 1
```

## Syntax Pattern

高频句式：

- “不是……而是……”
- “你以为……？”
- “我只是……”
- “这辈子……”
- “上辈子……”
- “对我来说，已经不重要了。”

女主关键句偏冷静、短促、结论先行：

- “是。”
- “所以我们退婚。”
- “因为你不行。”
- “我不愿意。”
- “不好奇。也不想试。”

傅沉舟句式偏自恋误判：

- “你闹够了没有？”
- “你以为这招欲擒故纵对我有用吗？”
- “你还喜欢我，对不对？”

林知意句式承担真相和价值转向：

- “因为我也一样。”
- “这辈子我要好好的为自己而活。”
- “没有傅沉舟，我林知意照样过得风生水起。”

## Scene Texture

视觉锚点密集但不铺陈：

- 棺材：公开羞辱物。
- 收购合同：反杀身份牌。
- 婚戒：前世流产创伤。
- 星星罐：错付真心证据。
- 咖啡杯：女性和解物。
- 手机消息：后段轻喜剧式补刀。

## Anti-AI Rules

- 不写“她内心五味杂陈”一类总结。
- 不用大段解释傅沉舟心理，必须让他通过台词暴露自恋。
- 不把顾宴京写成霸总救场机器，他的核心动作是询问和等待。
- 不让林知意继续雌竞到结尾，她必须承担价值观反转。
- 不用长段旁白替代婚礼、酒吧、咖啡馆等正面交锋。
