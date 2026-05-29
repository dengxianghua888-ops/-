# Style DNA

## 机器可读指标

统计口径：正文非空字符约12157，非空可视行约813行，按移动端可视行切分。

{
  "avg_sentence_chars": 15.79,
  "avg_visual_line_chars": 14.93,
  "median_visual_line_chars": 14.0,
  "short_line_rate_lte_16": 0.6617,
  "very_short_line_rate_lte_8": 0.196,
  "long_line_rate_gte_40": 0.0123,
  "direct_dialogue_line_rate": 0.2202,
  "barrage_line_rate": 0.2162,
  "dialogue_ratio_quote_lines": 0.2987,
  "dialogue_ratio_quote_content": 0.2126,
  "question_mark_density_per_1000_chars": 7.25,
  "exclamation_density_per_1000_chars": 8.82,
  "question_mark_count": 88,
  "aphorism_density_per_1000_chars": 0.74,
  "aphorism_count_estimated": 9,
  "barrage_commentary_role": "高频弹幕承担吐槽、误导、剧透卡顿和读者嘴替",
  "pace_lock": "快节奏锁定"
}

## 一句话风格定性

短行、高弹幕、高对话、轻喜剧反射弧。虐点被控制在误会和后怕里，释放方式永远是具体动作：转钱、送汤、递水、按脚、B超单、挡在身前、重新求婚。

## 句法特征

- 主叙述句普遍短，常用“我看着”“我想了想”“我点头”推动。
- 喜剧来自女主慢半拍回答，不来自段子解释。
- 男主情绪靠身体反应写出：眼眶红、喉结滚动、手指轻颤、吐血、攥皱B超单。
- 弹幕多用短促口语：“卧槽”“等等”“许总哭了”“这男人是真的爱惨了”。
- 每个高情绪节点后接一个女主清奇逻辑降温，防止过虐。

## 高频句式

1. 迟钝确认式  
“我眨了眨眼。”  
“我想了想。”  
“我慢吞吞地说。”

2. 弹幕误导式  
“【白月光快出来安慰他！】”  
“【等等，他真破产了啊？】”  
“【许这个姓……京城那个许家？】”

3. 男主深情证据式  
“他眼眶微红。”  
“手指在桌沿轻轻敲了两下。”  
“握得很紧，像怕我跑了。”

4. 清奇反杀式  
“照片能送我吗？我想留个纪念。”  
“孩子又没得罪我。”  
“我是贫血，不是吓的。”

## 金句与记忆点

| 类型 | 原文例句 | 功能 |
|---|---|---|
| 人设金句 | “孩子又没得罪我。” | 女主迟钝但善良 |
| 深情金句 | “从没想过放手。” | 男主真实动机 |
| 求婚金句 | “这一次，是余生。” | 仪式感 payoff |
| 回环金句 | “把你爸爸‘捡’回来了一辈子。” | 开篇捡人反转为终身选择 |
| 弹幕收束 | “她依然微醺，他依然宠溺。” | 读者情绪封口 |

## rhythm_contract

{
  "allowed_avg_visual_line_chars": [13, 18],
  "strict_avg_visual_line_chars": [12, 17],
  "short_line_rate_lte_16_min": 0.58,
  "short_line_rate_lte_16_max": 0.80,
  "very_short_line_rate_lte_8_max": 0.30,
  "long_line_rate_gte_40_max": 0.04,
  "direct_dialogue_line_rate_min": 0.18,
  "direct_dialogue_line_rate_max": 0.35,
  "barrage_line_rate_min": 0.12,
  "barrage_line_rate_max": 0.32,
  "dialogue_ratio_quote_lines_min": 0.25,
  "question_mark_density_per_1000_chars_min": 4.0,
  "question_mark_density_per_1000_chars_max": 10.5,
  "overcrank_forbidden": ["连续逼问", "每章黑屏", "每句都卡钩", "对白替代弹幕", "强压迫词堆叠"],
  "barrage_or_commentary_interval_chars": [180, 450],
  "micro_hook_interval_chars": [600, 1000],
  "chapter_min_hooks": 2,
  "chapter_min_question_or_reversal_prompt": 1,
  "chapter_min_evidence_flip": 1,
  "chapter_end_flat_close_allowed": false
}

## 快节奏锁定

快节奏锁定：仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。

执行要求：
- 每章必须有现场人物对峙、弹幕误导、甜宠证据或信息翻转。
- 每章必须有低压呼吸点：女主慢半拍反应、生活照顾动作、弹幕吐槽或轻喜剧错位。不能从头到尾都是逼问、宣告、崩溃、黑屏。
- 弹幕是源文的节奏发动机之一,不是装饰。每章至少保留 2-4 条弹幕/评论,且不要全部用问句。
- 情绪不能写成“我很难过”“他很爱我”，必须落到物件和动作：协议、工资短信、保温桶、报告袋、B超单、文件袋、戒指、婴儿床。
- 白月光挑衅必须当场被噎或被男主切割，不能拖成长虐。
- 豪门身份不能靠旁白说明完，必须通过老宅、管家、院子、项目洗牌、公开护短显影。
