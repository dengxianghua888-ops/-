# Style DNA

## 叙事外观
人称：第一人称女主视角。
语气：迟钝、慢半拍、轻喜剧、低解释。
场景切换：离婚桌前、别墅门口、工地、医院、病房、许家老宅、花园、产房。
核心表达方式：短句 + 对话 + 弹幕吐槽 + 具体动作。

## 机器可读数值
```json
{
  "source_length_chars_est": 16000,
  "avg_sentence_length_chars": 13.8,
  "avg_visual_line_length_chars": 18.5,
  "short_line_rate_lte_16_chars": 0.54,
  "long_line_rate_gte_40_chars": 0.06,
  "direct_dialogue_line_rate": 0.34,
  "bullet_comment_line_rate": 0.18,
  "dialogue_share": 0.39,
  "question_mark_density_per_1000_chars": 5.2,
  "exclamation_mark_density_per_1000_chars": 9.8,
  "golden_sentence_density_per_1000_chars": 1.4
}
```

## 行文节奏
1. 每个小节开头通常快速进入新场景，不铺垫环境。
2. 情绪峰值用短句切碎，例如“血。/ 从他指缝间渗出来。”
3. 女主反应常用“我眨了眨眼”“我想了想”“慢吞吞地说”形成稳定人设锚。
4. 男主情绪用身体反应呈现：眼眶红、喉结滚动、手指发抖、吐血、攥皱B超单。
5. 弹幕承担读者嘴替，负责吐槽、催促、补充误导、放大情绪，不替代主叙事。

## 高频句式
- “我想了想。”
- “我眨了眨眼。”
- “他眼眶红了。”
- “弹幕炸了：”
- “【……】”
- “我慢吞吞地说：”
- “许昀年愣了一下。”
- “不是……只是……”

## 金句/记忆点
- “孩子又没得罪我。”
- “我是他前妻，肚子里怀着他的孩子。”
- “从没想过放手。”
- “你愿意再嫁我一次吗？”
- “把你爸爸‘捡’回来了一辈子。”
- “她依然微醺，他依然宠溺。”

## 弹幕风格
弹幕必须像真实读者即时反应：
- 短。
- 口语。
- 有情绪。
- 可吐槽但不长篇解释。
- 常用“？？？”“！！！”“卧槽”“哈哈哈哈”“我哭死”。

弹幕功能分配：
- 误导：白月光回国、女配是替身。
- 加压：女主快说话、男主要碎了。
- 爽点放大：白月光被怼、许总切割。
- 悬念投喂：京城许家、男主真实身份。
- 结尾陪伴：完结撒花、祝福角色。

## rhythm_contract
```json
{
  "avg_visual_line_length_range": [15, 22],
  "short_line_rate_range": [0.45, 0.62],
  "direct_dialogue_line_rate_range": [0.28, 0.42],
  "bullet_comment_line_rate_range": [0.12, 0.24],
  "question_mark_density_per_1000_chars_range": [3.5, 7.0],
  "exclamation_mark_density_per_1000_chars_range": [6.0, 13.0],
  "min_hooks_per_chapter": 1,
  "min_rhetorical_or_question_turns_per_chapter": 1,
  "min_evidence_reversal_per_chapter": 1,
  "max_explanatory_paragraph_chars": 90,
  "preferred_dialogue_sentence_max_chars": 18
}
```

## 快节奏锁定
原文属于快节奏短篇。仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。误会、挑衅、甜宠、揭露都必须通过对话、动作、弹幕和物件证据现场发生。
