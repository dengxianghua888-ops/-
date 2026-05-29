# Style DNA

## 机器可读指标

```yaml
source_style_metrics:
  estimated_source_length_chars: 15500
  average_sentence_length_chars: 18.6
  average_visible_line_length_chars: 21.4
  short_line_rate_lte_16_chars: 0.46
  long_line_rate_gte_40_chars: 0.09
  direct_dialogue_line_rate: 0.43
  bullet_comment_line_rate: 0.04
  dialogue_char_ratio: 0.47
  question_mark_density_per_1000_chars: 5.2
  exclamation_mark_density_per_1000_chars: 4.1
  aphorism_density_per_1000_chars: 1.7
  chapter_like_hook_density_per_1000_chars: 1.3
  dominant_sentence_mode: "短句推进 + 对白打脸 + 证据清单式爆破"
  fast_pace_lock: true
```

## Opening Structure

```yaml
opening_structure: "conflict_first"
opening_summary_lines: 0
opening_summary_chain: []
opening_first_15_lines_function:
  - "第1行：第七次离婚传票落入亲子吃饭场景，直接冲突"
  - "第2-4行：主角安慰女儿争抚养权，建立父亲动机"
  - "第5行：女儿发问'卖多少钱'，亲情背刺"
  - "第6-9行：女儿拿出离婚协议，逼签"
  - "第10-12行：一百万财产划分和'辰辰叔叔'出现"
  - "第13-15行：情夫身份、五年坚持、女儿替母离婚完成核心痛点"
```

源文不是 `conclusion_first`。它没有在前10-15行冷静剧透完整反杀链，而是直接进入火锅店冲突现场。开篇结构为 `conflict_first`，局部夹杂对白爆钩。

## 快节奏锁定

源文属于快节奏短篇。仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。

必须保留：

- 每800-1200字一个新误判、新证据或新场面爆点。
- 亲密关系冲突优先通过对白和动作爆出，不用旁白概括“我很伤心”。
- 证据链必须在现场被看见：协议、转账、视频、电话、庭审材料、判决。
- 每次主角心软前都要插入更狠背刺，逼他更冷静。

## Rhythm Contract

```yaml
rhythm_contract:
  average_visible_line_length_chars:
    min: 18
    max: 25
  short_line_rate_lte_16_chars:
    min: 0.38
    max: 0.55
  long_line_rate_gte_40_chars:
    min: 0.04
    max: 0.12
  direct_dialogue_line_rate:
    min: 0.35
    max: 0.52
  bullet_comment_line_rate:
    min: 0.02
    max: 0.08
  question_mark_density_per_1000_chars:
    min: 3.5
    max: 7.0
  exclamation_mark_density_per_1000_chars:
    min: 2.0
    max: 5.5
  minimum_hooks_per_chapter: 1
  minimum_rhetorical_questions_per_chapter: 1
  minimum_evidence_reversal_per_3000_chars: 1
  minimum_public_execution_scenes: 2
  maximum_expository_paragraph_chars: 90
```

## 句法特征

1. 短句后置刺痛  
   例：“算多给了。”、“又是一张卡。”、“好一个没有逼我。”

2. 对白即刀  
   重要情绪不由旁白解释，而由人物说出荒谬价值观：
   - “你要把我卖多少钱才开心呀？”
   - “我又没有逼你。”
   - “跪在地上捡吧，周时安。”

3. 证据清单推进  
   源文的爽点经常用账单、转账、消费记录、庭审证据推进，而不是主角口嗨：
   - 千万别墅转账
   - 八十万月子中心
   - 八千万第三者转账
   - 公司资产冻结
   - 未受益证明

4. 公开场面升级  
   私人羞辱不会私了，必须转入更大观众席：
   - 公司前台
   - 学校老师和同学
   - 发布会媒体资方
   - 庭审旁听席

## 金句模型

源文金句不是文学化，而是规则回旋式短句：

- “好一个懂事的女儿。”
- “好一个没有逼我。”
- “她，连同你这个人，我都不要了。”
- “你不是突然想起又爱我了，你只是怕没人照顾你了。”
- “我没有做什么，分明是你，坏事做尽，才自食其果。”

仿写金句要求：

- 每句不超过28字。
- 优先用反派原话回旋。
- 不要写抽象鸡汤。
- 结尾金句必须服务“不原谅”或“规则反杀”。

## 视角与语气

```yaml
narration:
  pov: "第一人称受害者视角"
  tone: "冷静、克制、被伤透后的低温"
  emotional_display: "前期忍痛压抑，中段彻底失望，后期法律化清算"
  forbidden_tone:
    - "大段哭诉"
    - "圣父式自我感动"
    - "复仇宣言式中二台词"
    - "解释型长心理分析"
```
