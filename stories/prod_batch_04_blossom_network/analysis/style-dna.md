# Style DNA

## Machine-readable Metrics

```json
{
  "source_length_chars_raw_body": 14948,
  "source_length_chars_no_whitespace": 14001,
  "section_count": 36,
  "sentence_count_punctuation_based": 887,
  "avg_sentence_length_chars": 14.71,
  "median_sentence_length_chars": 13,
  "line_unit_count": 851,
  "avg_line_unit_length_chars": 15.79,
  "median_line_unit_length_chars": 13,
  "dialogue_segment_count": 251,
  "dialogue_chars_no_whitespace": 3964,
  "dialogue_ratio": 0.2831,
  "question_count": 53,
  "question_density_per_1000_chars": 3.79,
  "exclamation_count": 47,
  "exclamation_density_per_1000_chars": 3.36,
  "golden_sentence_count_estimated": 16,
  "golden_sentence_density_per_1000_chars": 1.14,
  "short_line_ratio_le_16_chars": 0.6287,
  "short_line_ratio_le_20_chars": 0.7673,
  "quote_line_ratio": 0.2891,
  "named_entity_frequency": {
    "顾斯越": 105,
    "外婆": 75,
    "夏晚星": 47,
    "温希": 40,
    "醒醒": 37,
    "顾砚醒": 20,
    "朵朵": 11,
    "德国": 7,
    "陈医生": 4
  }
}
```

## 句法 DNA

- 主体是第一人称冷叙述，短句密集，平均句长约 14.71 字。
- 大量单行短句制造“情绪断裂感”，例如第 1 节：
  - “原来他一直都知道。”
  - “我有多想嫁给他。”
  - “这七年。”
  - “现在为了夏晚星。”
  - “他要娶我了。”
- 情绪峰值不靠长篇控诉，而靠短句连续下坠。
- 重要决定常用三段式短句落锤：
  - 第 8 节：“顾斯越。顾砚醒。我都不要了。”
  - 第 20 节：“顾斯越。自愿生生世世。永不再相见。”
  - 第 34 节：“但是，我不爱你了。”

## 对话 DNA

- 对话占比约 28.31%，高于纯叙述虐文，符合番茄短篇的强冲突节奏。
- 对话功能分三类：
  1. 公开羞辱：开篇兄弟局、公司会议、主宅对峙。
  2. 迟到补救：顾斯越事后解释、道歉、求回家。
  3. 真相引爆：外婆信、醒醒读信后的追问、助理电话。
- 男主前期台词冷、短、命令式：
  - “摆正你的位置。”
  - “温希，别再闹了。”
- 女主后期台词冷、准、边界清晰：
  - “七年前，我想要一个家，你不愿意给。”
  - “现在，我不需要了。”
  - “他不是你追回我的工具。”
  - “但是，我不爱你了。”

## 问号与爆点

- 问号密度 3.79/千字，主要集中在争执和追悔段。
- 前半段问号用于压迫女主：
  - “你外婆，和我关系是？”
  - “想当周太太？”
  - “你很缺钱？”
- 中段问号用于女主爆发：
  - “为什么？”
  - “你凭什么欺负我外婆？”
- 后半段问号用于男主和孩子崩塌：
  - “妈妈是不是……不要我们了？”
  - “你就真的……一点机会都不肯给我了吗？”

## 金句 DNA

估算金句密度约 1.14/千字。金句不追求华丽，而是“短、冷、不可逆”。

高价值样本：

- 第 1 节：“七年的执念化为灰烬。”
- 第 6 节：“醒醒的洁癖。是分人的。”
- 第 8 节：“顾斯越。顾砚醒。我都不要了。”
- 第 12 节：“从今往后，山高水长。不必再见。”
- 第 19 节：“我的希希，自己就是自己的依靠。”
- 第 20 节：“自愿生生世世。永不再相见。”
- 第 30 节：“不爱，不恨，甚至……连一点涟漪都没有。”
- 第 31 节：“他不是你追回我的工具。”
- 第 34 节：“这条命是你给的，如果有下辈子，我会还给你。但是，我不爱你了。”
- 第 35 节：“终于迎来了属于自己的春暖花开。”

## 场景 DNA

- 场景切换快，每个场景只承载一个核心伤害或一个核心决定。
- 高频场景类型：
  - 包厢：偷听羞辱，开局高压。
  - 医院：外婆病情、亲情债、真相信件。
  - 公司会议室：白月光公开压迫。
  - 幼儿园：孩子线崩裂。
  - 主宅：归属权被夺。
  - 律所：协议误判与女主拿资源。
  - 机场：断联离开。
  - 德国：新生与拒绝追妻。
- 每个关键场景都有一个物件锚定情绪：酒杯、合同、垃圾桶、签证、指纹锁、戒指、信封、SIM 卡、股权协议。

## 改编执行参数

```json
{
  "target_sentence_length_chars": "12-18",
  "target_dialogue_ratio": "0.25-0.32",
  "target_question_density_per_1000_chars": "3.0-4.5",
  "target_golden_sentence_density_per_1000_chars": "1.0-1.5",
  "target_short_line_ratio_le_16_chars": ">=0.55",
  "required_scene_object_anchor": true,
  "required_late_truth_material": true,
  "forbid_long_expository_grief": true,
  "forbid_easy_reconciliation": true
}
```
