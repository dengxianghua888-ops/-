# Style DNA

## 机器可读指标

```yaml
source_title: 被四个女生举报开除，我失联后，她们哭着全世界找我
estimated_source_length_chars: 15800
opening_structure: conclusion_first
opening_summary_lines: 11
average_sentence_length_chars: 18.5
average_visible_line_length_chars: 27.8
short_line_rate_lte_16_chars: 0.37
long_line_rate_gte_40_chars: 0.16
direct_dialogue_line_rate: 0.30
barrage_comment_line_rate: 0.08
dialogue_ratio_by_visible_lines: 0.34
question_mark_density_per_1000_chars: 2.7
exclamation_mark_density_per_1000_chars: 2.2
golden_sentence_density_per_1000_chars: 1.1
pace_lock: true
```

## 开篇结构分析

- `opening_structure`: `conclusion_first`
- `opening_summary_lines`: 11
- 前置摘要覆盖的逻辑链：
  - 极端处境：好心给学生买冰箱，药失效，学生终身残疾。
  - 荒谬行为：家长拉横幅骂“黑心老师”，还要求主角娶她、养一辈子。
  - 反击方式：重生回到第一次请求时，主角只让她走后勤流程。
  - payoff 预告：同样节点换选择，暗示责任会回到真正制造问题的人身上。

## 快节奏锁定

源文是快节奏短篇，仿写必须锁定以下节奏：

- 不得用解释性长段替代现场交锋。
- 不得用流程清单替代对话冲突。
- 不得用情绪总结替代证据翻转。
- 每 800-1200 字必须出现新风险、新谣言、新证据或新责任归属。
- 主角的心理可以冷，但场面必须动：举报、谈话、直播、围堵、调查、公开视频持续推进。

## 句法特征

1. **短句压迫开局**  
   开篇大量单句成段：“半个月后，药失效了。”“她倒在教室，终身残疾。”  
   功能是用事实砸读者，不给喘息。

2. **冷静旁白 + 尖锐吐槽**  
   主角叙述基本冷静，但会突然插入强烈判断，如“草台班子”“毁灭吧”“她们，每个都是凶手”。  
   功能是让读者站队。

3. **对话推动剧情**  
   系主任、校长、李婷、周小月、金毛网红、警察的对话都承担反转推进，几乎没有空转聊天。

4. **互联网文本嵌入**  
   标题、弹幕、直播间评论、热搜式句子反复出现，让爽点公开化、围观化。

5. **金句回旋**  
   “现在，轮到她了。”是全篇情绪回旋核心，把前世主角一家遭遇的网暴返还给周小月。

## rhythm_contract

```yaml
final_average_visible_line_length_range_chars: [23, 32]
short_line_rate_lte_16_chars_range: [0.32, 0.48]
long_line_rate_gte_40_chars_max: 0.20
direct_dialogue_line_rate_range: [0.25, 0.38]
barrage_comment_line_rate_range: [0.05, 0.12]
dialogue_ratio_by_visible_lines_range: [0.30, 0.42]
question_mark_density_per_1000_chars_range: [1.8, 4.0]
exclamation_mark_density_per_1000_chars_range: [1.2, 3.2]
min_hooks_per_chapter: 2
min_rhetorical_questions_per_chapter: 1
min_evidence_flip_per_chapter: 1
paywall_card_interval_chars: [2500, 3500]
```

## 禁用风格

- 禁止连续 3 段以上解释背景。
- 禁止“我很痛苦、我很愤怒”式抽象情绪总结。
- 禁止把直播弹幕写成整齐评论区分析，要短、乱、狠。
- 禁止让主角长篇说教，主角最爽的姿态是少解释、留证据、等反噬。
- 禁止使用“命运”“宿命”“救赎”等泛化大词冲淡现实爽点。
