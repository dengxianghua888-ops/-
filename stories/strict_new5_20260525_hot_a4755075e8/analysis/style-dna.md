# Style DNA

## 1. 机器可读指标

```yaml
source_body_chars: 11119
nonempty_lines: 655
sentence_count: 677
avg_sentence_len_chars: 15.4
avg_visual_line_len_chars: 16.98
short_line_rate_le_16: 0.5527
long_line_rate_ge_40: 0.0260
direct_dialogue_line_rate: 0.2412
danmu_comment_line_rate: 0.0061
dialogue_ratio_by_chars: 0.2641
question_mark_density_per_1k_chars: 4.32
exclamation_mark_density_per_1k_chars: 0.00
golden_line_density_per_1k_chars: 1.17
estimated_golden_lines:
  - "你定的规则不是我选的，如果你想结束，可以，但条件由我来说。"
  - "什么都没碎，但什么也都碎了。"
  - "刀是他自己拿起来的。"
  - "我原谅你，但我不会回来了。"
  - "碎了的花瓶粘起来也是裂的。"
  - "不是给谁的回应。是给自己的。"
```

说明：
- `avg_sentence_len_chars` 很短，说明文本主要靠句切推进，不靠长复句。
- `avg_visual_line_len_chars` 贴近 17 字，属于典型番茄女频短篇快推流。
- `short_line_rate` 超过 55%，说明大量使用单独成行的动作、顿点、反问、回弹句。
- `direct_dialogue_line_rate` 与 `dialogue_ratio_by_chars` 都不低，证明现场交锋是主驱动力。
- `question_mark_density` 高，说明文本频繁用反问、追问、质问制造读者跟读。
- `exclamation_mark_density` 为 0，是重要特征：全篇不用喊叫制造激烈，而靠冷静和断句制造杀伤。

## 2. 节奏体感拆解

### 2.1 句法
- 主句短，常见 8-18 字。
- 高密度单行句：
  - “我没签。”
  - “发送。”
  - “家里。”
  - “客房。”
  - “没松手。”
- 作用：把情绪敲成钉子，不给抒情漫流空间。

### 2.2 对话
- 对话不是闲聊，是每次都携带新证据或新刀子。
- 典型台词都很短，且带角色判断：
  - 小三台词负责炫耀和踩脸。
  - 男主台词负责威胁和补偿性温度。
  - 女主台词负责冷处理和价值判决。

### 2.3 描写
- 少形容词，多物件：
  - 戒指
  - 翡翠镯
  - 美式
  - 酸汤鱼
  - 账单
  - 流水
  - 碎玉
  - 护手霜
- 物件既是情绪载体，也是证据锚点。

### 2.4 情绪控制
- 极少出现“我崩溃了”“我很痛”这类总结句。
- 常用身体反应替代抽象情绪：
  - “手指开始发抖”
  - “膝盖一软”
  - “脸上什么表情都没有”
  - “呼吸猛地顿了一下”
- 这让文本更像现场录像，不像情绪汇报。

## 3. 金句结构

高频金句模板：
1. `不是A，是B`
   - “不是舍不得。是我在把这种疼一寸一寸刻进骨头里。”
2. `A没碎，但B碎了`
   - “什么都没碎，但什么也都碎了。”
3. `不是X毁了我们，X只是递了一把刀`
   - “刀是他自己拿起来的。”
4. `我可以原谅，但不会回头`
   - “我原谅你，但我不会回来了。”
5. `物件无法复原 = 关系无法复原`
   - “碎了的花瓶粘起来也是裂的。”

可见该文金句不是华丽修辞，而是极简判断句。

## 4. 叙事合同

### 快节奏锁定
本篇为明确快节奏短篇，仿写必须锁定：

- 不得使用解释性长段替代现场交锋。
- 不得用流程清单替代“证据一条条落地”。
- 不得在关键冲突处改成内心独白大段抒情。
- 每个章节都要有可见动作、可见物件、可见站队。

### rhythm_contract

```yaml
avg_visual_line_len_allowed: [15.5, 19.5]
short_line_rate_allowed: [0.48, 0.65]
direct_dialogue_line_rate_allowed: [0.20, 0.32]
danmu_comment_line_rate_allowed: [0.003, 0.02]
question_mark_density_per_1k_allowed: [3.2, 5.5]
exclamation_mark_density_per_1k_allowed: [0.0, 0.5]
min_hooks_per_chapter: 1
min_rhetorical_questions_per_chapter: 1
min_evidence_reversals_per_chapter: 1
min_public_or_interpersonal_confrontations_per_3_chapters: 2
```

## 5. 风格底层规则

1. 每次新信息出现，最好附着在一个具体载体上。
2. 每次情绪升高，不用感叹号，而用停顿和短句。
3. 每个“温柔”后面最好跟一刀，形成温度反转。
4. 女主不能说教，必须冷而准。
5. 男主的悔不是靠独白解释，而是靠看见账单、旧物、碎片、录音、照片后失语。
6. 结尾必须轻，不喊口号；收在“她重新拥有自己”。
