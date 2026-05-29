# Style DNA

## 总体判断
- 类型：强对白、强动作、强短句、强章尾钩的番茄都市女频快节奏短篇
- 叙述人称：第一人称主叙，穿插少量回忆
- 语言气质：口语化、可视化、低修辞、高冲突
- 快节奏锁定：**仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。**

## 机器可读指标
```json
{
  "avg_sentence_len_chars": 16.9,
  "avg_visual_line_len_chars": 18.7,
  "short_line_rate_le_16": 0.56,
  "long_line_rate_ge_40": 0.05,
  "direct_dialogue_line_rate": 0.47,
  "danmu_comment_line_rate": 0.00,
  "dialogue_ratio": 0.62,
  "question_density_per_1000_chars": 4.6,
  "exclamation_density_per_1000_chars": 6.9,
  "golden_line_density_per_1000_chars": 2.1,
  "flashback_ratio": 0.18,
  "chapter_end_hook_rate": 0.90
}
```

## 指标解释
- `avg_sentence_len_chars 16.9`
  - 句子多为10-20字短句，少量回忆句会拉长平均值。
- `avg_visual_line_len_chars 18.7`
  - 明显按手机阅读切行设计，一行一刀，适合追更与付费页翻动。
- `short_line_rate 0.56`
  - 超过一半行长不超过16字，利于“台词砸脸”。
- `long_line_rate 0.05`
  - 长行很少，主要出现在回忆说明或结果交代。
- `direct_dialogue_line_rate 0.47`
  - 近一半为直接对白行，冲突靠人物嘴里打出来。
- `dialogue_ratio 0.62`
  - 文本主体不是叙景，而是对话推进。
- `question_density`
  - 问句主要用于羞辱、逼问、否认与挑衅。
- `exclamation_density`
  - 感叹号用于现场情绪抬升和钩子处放大冲击。
- `golden_line_density`
  - 平均每500字左右有一句可截屏金句或反杀句。

## 节奏合同 `rhythm_contract`
```json
{
  "avg_visual_line_len_range": [16, 22],
  "short_line_rate_range": [0.48, 0.65],
  "direct_dialogue_line_rate_range": [0.40, 0.55],
  "danmu_comment_line_rate_range": [0.00, 0.03],
  "question_density_per_1000_chars_range": [3.5, 6.0],
  "min_hooks_per_chapter": 1,
  "min_rhetorical_questions_per_chapter": 1,
  "min_evidence_reversals_per_chapter": 0.5,
  "min_identity_pressure_turns_per_3_chapters": 2
}
```

## 句法与行文特征
- 高频结构：
  - `短动作 + 短台词`
  - `反问句 + 人名点名`
  - `旧账回忆 + 当场反差`
  - `一记动作/一句话/一个物件`完成翻盘推进
- 高频口语刀法：
  - “你疯了？”
  - “你什么意思？”
  - “你凭什么？”
  - “那就好。”
  - “太晚了。”
- 高频具象道具：
  - 户口本、红本本、婚纱、戒指、伴娘服、劳斯莱斯、热搜、清宫同意书
- 高频身体反应：
  - “眼眶红了”
  - “嘴唇哆嗦”
  - “手抖得几乎握不住”
  - “眼泪砸在地上”

## 修辞偏好
- 不靠华丽比喻取胜，靠“伦理荒唐感”取胜。
- 比喻只做点到即止，如：
  - “像逗弄不听话的狗”
  - “像一把刀扎进心口”
- 金句必须短、硬、可转发，不写散文化大段抒情。

## 结构型风格基因
- 前300字必须双反常：
  - 婚姻资格被抢
  - 女主反手换人
- 每章必须新增一种失衡：
  - 身份失衡
  - 情感失衡
  - 家族站位失衡
  - 现实资源失衡
- 回忆段不独立成块，必须服务于当前羞辱或当前反打。
- 现任的深情不能长篇表白，必须体现在“早准备、真执行、公开接住”。

## 禁区
- 不能把对白改写成长心理分析。
- 不能让女主大段讲道理。
- 不能把现任写成温吞守护型。
- 不能让章节中段空转，只铺情绪不出新信息。
- 不能用商战流程替代情感清算，债务回收只需够狠够清楚，不需专业展开。
