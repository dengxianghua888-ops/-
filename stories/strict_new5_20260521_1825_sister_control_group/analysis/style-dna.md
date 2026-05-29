# Style DNA

## 叙事外观
- 人称：第一人称女主自述。
- 题材气质：家庭伦理重生爽文，校园到成年长线跨越。
- 核心表达方式：短段推进 + 对话锚点 + 回看式认知修正 + 少量金句回收。
- 场景切换方式：介绍现场、食堂、教室、水房、放学路、医院、粥铺、娘家、小区门口，全部直接切入，不铺环境大段。

## 机器可读数值
```json
{
  "source_length_chars": 10745,
  "avg_sentence_length_chars": 17.3,
  "avg_visual_line_length_chars": 23.3,
  "short_line_rate_lte_16_chars": 0.335,
  "long_line_rate_gte_40_chars": 0.104,
  "direct_dialogue_line_rate": 0.271,
  "bullet_comment_line_rate": 0.0,
  "dialogue_share": 0.309,
  "question_mark_density_per_1000_chars": 3.91,
  "exclamation_mark_density_per_1000_chars": 0.28,
  "golden_sentence_density_per_1000_chars": 1.95
}
```

## 高频外观特征
- 常用“原来”“现在想来”“闻此”“这次重来”触发认知翻案。
- 段落长度普遍短，常 1-3 句一段，便于密集抛钩。
- 对话承担信息揭露，旁白承担“旧细节重解释”。
- 环境描写少，只在恋爱舒缓段给一点轻风、眼镜、耳尖发红之类的软化物。
- 评论/弹幕行率为 0，说明它不是靠外部嘴替，而是靠女主自身清醒得出结论。

## 节奏规律
1. 每次重大情绪波动，都会用一条具体物证或一句话落锤。
2. 钩子间距短，几乎每 600-1000 字就有一次新信息升级。
3. 解释段虽然存在，但常紧跟在爆点后，功能是“重释旧细节”，不是空抒情。
4. 校园期用“分班、补课、志愿、排名”这些硬节点推动；成年期用“怀孕、婚礼、举报、离婚、报警”这些社会节点推动。
5. 男角色对照主要靠行为差异，不靠旁白评判：
   - 陆霄：堵人、搂、按墙、双向占有、求复合后施暴。
   - 方彦：补习、递面、记过敏、接电话、报警挡人。

## 高频句式
- “现在想来……”
- “原来……”
- “这次，我没再……”
- “闻此……”
- “我瞥了他一眼……”
- “我冷冷看着他……”
- “我气得……”
- “我叹了口气……”

## 金句密度与类型
- 密度偏中高，不是句句立碑，而是在关键价值节点落句。
- 代表句：
  - `134` “争男人没意思，和男人争排名才有意思。”
  - `317` “陆霄是她的备胎，而我是备胎的备胎。”
  - `415` “女人只有自强自立，才能拥有真正的幸福。”
  - `434` “人不能踏入同一条河流两次，我也不会在同一个男人身上栽两次。”

## rhythm_contract
```json
{
  "avg_visual_line_length_range": [20, 27],
  "short_line_rate_range": [0.28, 0.40],
  "direct_dialogue_line_rate_range": [0.22, 0.33],
  "bullet_comment_line_rate_range": [0.0, 0.03],
  "question_mark_density_per_1000_chars_range": [3.0, 5.5],
  "exclamation_mark_density_per_1000_chars_range": [0.0, 1.2],
  "min_hooks_per_chapter": 1,
  "min_rhetorical_or_question_turns_per_chapter": 1,
  "min_evidence_reversal_per_chapter": 1,
  "max_explanatory_paragraph_chars": 120,
  "preferred_dialogue_sentence_max_chars": 24
}
```

## 快节奏锁定
原文属于快节奏短篇。仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。所有认知翻案都必须靠：
- 对话里抛出的新真相
- 物证级细节对照
- 女主当场做出的路线选择
- 关系现场的即时失态

## 改编时最容易丢的风格核
- 不能把女主写成一直大哭大闹，她的爽点在“后知后觉后迅速清醒”。
- 不能让方彦变成拯救者，他的写法要始终轻、稳、记得细节。
- 不能让价值表达过早端出来，必须在大爆点后自然落句。
- 不能把医院偷听写成旁白总结，必须保留门外偷听的生理冲击感。
