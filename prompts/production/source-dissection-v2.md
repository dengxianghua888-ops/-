# Source Dissector V2 Contract

你要把原文拆成可执行的爆款工程数据。必须输出:
- `story-brief.json`
- `dissection.md`
- `analysis/beat-sheet.md`
- `analysis/style-dna.md`
- `analysis/soul-contract.md`
- `analysis/reader-engine.md`
- `analysis/tension-ledger.md`
- `analysis/chapter-soul-map.json`

`story-brief.json` 必须包含:
- `source_title`, `genre`, `hook_type`, `title_formula`
- `reversal_mechanisms`
- `source_length_chars`
- `reader_promise`
- `emotional_debts`
- `payoff_pattern`
- `forbidden_to_change`
- `replaceable_assets`

Schema 硬要求:
- `hook_type` 必须是非空字符串,不要写成对象。
- `title_formula` 必须是非空字符串,不要写成对象。
- `payoff_pattern` 必须是非空字符串,可以用分号串联关键节奏,不要写成数组。
- `reversal_mechanisms`, `emotional_debts`, `forbidden_to_change`, `replaceable_assets` 必须是数组。

拆解要求:
- Beat 必须精确到原文段落/句子证据。
- 每个 Beat 必须有情绪强度、信息差、读者期待、章尾钩功能。
- Style DNA 必须给机器可读数值: 平均句长、平均可视行长、短行率(<=16字行占比)、长行率(>=40字行占比)、直接对白行率、弹幕/评论行率、对话占比、问号密度、感叹号密度、金句密度。
- Style DNA 必须写出 `rhythm_contract`: 终稿允许的平均可视行长区间、短行率上下限、直接对白行率上下限、弹幕/评论行率上下限、问号密度上下限、单章内最少钩子/反问/证据翻转次数。
- 若原文是快节奏短篇,必须标注"快节奏锁定": 仿写不得用解释性长段、流程清单、情绪总结替代现场交锋。
- 禁止只概括剧情。

开篇结构分析（必填,写入 `analysis/style-dna.md`）:
- 判断源文属于哪种开篇结构:
  - `conclusion_first`: 前 10-15 行冷静剧透完整故事逻辑链
  - `conflict_first`: 直接进入冲突场景
  - `dialogue_first`: 以对白开篇
- 标注字段 `opening_structure` 到 style-dna.md
- 若为 `conclusion_first`,同时标注 `opening_summary_lines`（摘要行数）和前置摘要覆盖的逻辑链要素

---

## 逐章神髓提取（V6 核心新增）

按原文的分章标记（`## 第X章`、`第X章`、`一、`等），逐章输出 `analysis/chapter-soul-map.json`。

若原文无分章标记，按约 800 字一章均匀切分，标注 `"auto_split": true`。

每章必须包含以下七个维度（缺一不可）：

### A. 节奏骨架（定量指标）

- `avg_line_chars`: 平均可视行字数
- `comma_period_ratio`: 逗号数/句号数
- `question_mark_density_per_1k`: 每千字问号数
- `direct_dialogue_rate`: 直接对白行占比
- `short_line_rate_lte16`: ≤16字行占比
- `impact_density`: 冲击密度
- `sentence_avg_len`: 平均句长（含逗号的完整句）

> 注: A 维度的定量指标由脚本 `chapter_soul_extractor.py` 预填充。你需要验证并修正明显异常值。

### B. 情绪神髓（必填）

- `dominant_emotion`：本章主导情绪（用 2-4 个字概括，如"屈辱-决绝"、"暗涌-爆发"）
- `emotion_arc`：本章情绪走向（如"平静 → 震惊 → 愤怒 → 冷静决断"）
- `emotion_intensity`：1-10 分，10 为极致情绪
- `reader_feeling_target`：读者读完本章应该有什么感受（一句话）

### C. 高光与爆点

- `peak_moment`：本章最强一击是什么（用一句话描述事件）
- `peak_type`：爆点类型标签（public_humiliation / truth_reveal / betrayal_stack / physical_violence / cold_revenge / emotional_bomb / power_shift / identity_reveal）
- `emotional_bomb`：情绪炸弹的具体内容
- `bomb_detonation_technique`：引爆手法（递进式 / 反转式 / 对比式 / 累积式 / 突变式）
- `reader_hook_point`：本章最让读者"停不下来"的那一刻

### D. 表现手法解剖（本章 Top 3-5 个最强手法）

每个手法必须包含：
- `technique`：手法名称（如"物件具象化"、"三段递进"、"冷静反差"、"降格比喻"、"时间压缩"）
- `example`：原文中的具体使用案例（引用原文）
- `effect`：这个手法为什么有效（对读者产生什么心理效果）

> 手法必须是"可复制的写作技巧"，不是"情节概括"。仿写时要复刻的是技巧本身，不是具体情节。
> 每章至少 3 个独立手法，全篇不得少于 15 个手法条目。
> 手法不能重复使用泛泛标签（不能所有章都写"递进"）——必须具体到该章独有的用法。

### E. 金句与句式（本章 Top 2-5 句）

每句必须标注：
- `text`：原文
- `structure`：句式结构模板（如"动作+反衬比喻"、"重复词+递进"）——必须是可套用的模板
- `why_it_works`：为什么这句话有力量（心理学层面）

### F. 叙事模式与节奏形状

- `narrative_mode`：conflict_first / emotion_buildup / revelation / chase_sequence / breathing / dialogue_driven
- `rhythm_shape`：本章的节奏形状（如"前慢后快"、"匀速高压"、"波浪起伏"、"蓄力-爆发"）
- `pacing_note`：节奏维持的核心手段（靠事件密度？靠对话节奏？靠情绪渲染？靠信息差？）

### G. 章末钩子

- `text`：章末钩子原文
- `hook_type`：钩子类型（death_declaration / cliff_action / revelation_half / question_bomb / contrast_shock / silent_threat / power_reversal）
- `hook_technique`：钩子的具体写法描述
- `suspense_mechanism`：这个钩子激发读者什么好奇心

---

## chapter-soul-map.json 输出格式

```json
{
  "chapters": [
    {
      "chapter_id": 1,
      "source_line_range": [1, 48],
      "char_count": 820,
      "auto_split": false,
      "metrics": {
        "avg_line_chars": 14.2,
        "comma_period_ratio": 0.45,
        "question_mark_density_per_1k": 3.2,
        "direct_dialogue_rate": 0.38,
        "short_line_rate_lte16": 0.72,
        "impact_density": 0.85,
        "sentence_avg_len": 18.5
      },
      "emotion": {
        "dominant_emotion": "屈辱-决绝",
        "emotion_arc": "震惊 → 隐忍 → 冷静决断",
        "emotion_intensity": 8.5,
        "reader_feeling_target": "替女主窒息，同时被她的冷静震撼"
      },
      "highlights": {
        "peak_moment": "描述",
        "peak_type": "public_humiliation",
        "emotional_bomb": "描述",
        "bomb_detonation_technique": "递进式",
        "reader_hook_point": "描述"
      },
      "techniques": [
        {
          "technique": "手法名",
          "example": "原文引用",
          "effect": "心理效果"
        }
      ],
      "golden_lines": [
        {
          "text": "原文",
          "structure": "句式模板",
          "why_it_works": "原因"
        }
      ],
      "narrative_mode": "conflict_first",
      "rhythm_shape": "匀速高压",
      "pacing_note": "靠事件密度维持张力",
      "chapter_end_hook": {
        "text": "原文",
        "hook_type": "death_declaration",
        "hook_technique": "写法描述",
        "suspense_mechanism": "激发什么好奇心"
      }
    }
  ],
  "global_soul_signature": "对全篇写作风格内核的一句话总结",
  "character_voices": [
    {
      "role": "角色名",
      "speech_pattern": {
        "avg_utterance_length": 8,
        "口癖": ["例1", "例2"],
        "语气词": ["呗", "嘛"],
        "句式特征": "一句话描述",
        "禁用词": ["不会说的词"],
        "情绪表达方式": "一句话描述",
        "典型台词示例": ["原文台词1", "原文台词2"]
      }
    }
  ]
}
```

---

## 角色语言画像提取（V6.1 新增）

在 `chapter-soul-map.json` 中新增顶层字段 `character_voices`（与 `chapters` 同级）：

```json
{
  "character_voices": [
    {
      "role": "角色名或角色功能（如'女主'、'渣男'、'婆婆'）",
      "speech_pattern": {
        "avg_utterance_length": 8,
        "口癖": ["你懂什么", "呸", "就是"],
        "语气词": ["呗", "嘛", "哎"],
        "句式特征": "极短、祈使句多、粗俗直白",
        "禁用词": ["然而", "况且", "因此"],
        "情绪表达方式": "不解释情绪，通过骂人和动作表达",
        "典型台词示例": ["有人生没人养的东西", "你算什么东西"]
      }
    }
  ]
}
```

提取规则：
- 每个有台词的角色都必须提取语言画像（至少 2 个角色）
- `avg_utterance_length` 是该角色单句平均字数（从原文统计）
- `口癖` 是反复出现的词/短语（3-5 个）
- `句式特征` 一句话概括这个人"怎么说话"（如"极短祈使句+骂人"或"绕弯式暗示+反问"）
- `禁用词` 列出这个角色绝不会说的词（如粗人不会说"况且/然而"，文化人不会说"呸/滚"）
- `典型台词示例` 引用原文中最有代表性的 2-3 句台词

---

## 提取质量要求

- Section D（表现手法）是最核心的输出——仿写时复刻的是"手法"而非"数值"
- 每章至少 3 个独立手法，全篇不得少于 15 个手法条目
- 手法不能重复使用泛泛标签——必须具体到该章独有的用法
- 金句的 `structure` 字段必须是可套用的模板，仿写时可以填入新内容产生同类效果
- `global_soul_signature` 一句话概括"这篇文为什么好看"的内核写法特征

## 输出前自检

- [ ] 每章 7 个维度全部填写？
- [ ] 全篇手法条目 ≥ 15？
- [ ] 每个手法有具体 example（引用原文）？
- [ ] 金句的 structure 是可套用模板？
- [ ] chapter_end_hook 每章都有？
- [ ] global_soul_signature 已填写？
- [ ] character_voices 已为每个有台词角色填写？（至少 2 个角色）
- [ ] 每个角色的 speech_pattern 包含口癖+典型台词示例？
