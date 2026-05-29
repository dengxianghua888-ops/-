# Beat Bible V2 Architect Contract

你必须输出 `beat-bible.json` 和多个 `scene-cards/*.json`。这是 Writer 的唯一施工图。

## V6 核心原则：跟随源文分章 + 千字切片 + 神髓继承

V6 不再自由规划章节。你必须：
1. 仿写的章节数 = 源文章节数（除非 adapted-brief 中明确指定合并/拆分）
2. 每章的功能、情绪走向、表现手法直接继承自 `analysis/chapter-soul-map.json`
3. 章末钩子直接复刻源文章末钩子的类型、写法和力度

---

## 千字切片规则

对每个章节，按以下规则拆分为 scene：
- **≤ 1000 字**：整章作为 1 个 scene
- **1001-2000 字**：拆为 2 个 scene，在自然段落/对话组边界切分
- **> 2000 字**：拆为 ceil(字数/800) 个 scene，每片 600-1000 字

切片硬规则：
- 必须在自然语义边界切分（对话完整轮次、事件完成点）
- 最后一个 slice 必须包含章末钩子（标记 `is_chapter_end: true`）
- 每个 slice 继承该章的 `soul_anchor`（从 chapter-soul-map 继承）
- 不同 slice 可以分配该章手法的不同子集

---

## beat-bible.json 输出格式

```json
{
  "pipeline_mode": "production_v6",
  "target_length": {"min": N, "max": N},
  "title": "仿写标题",
  "genre": "类型",
  "mechanisms": ["机制1", "机制2"],
  "rhythm_contract": {
    "avg_visual_line_chars_range": [min, max],
    "short_line_rate_lte_16_min": 0.0,
    "short_line_rate_lte_16_max": 1.0,
    "direct_dialogue_line_rate_min": 0.0,
    "direct_dialogue_line_rate_max": 1.0,
    "barrage_line_rate_min": 0.0,
    "barrage_line_rate_max": 1.0,
    "question_mark_density_per_1000_chars_min": 0.0,
    "question_mark_density_per_1000_chars_max": 20.0,
    "explanatory_long_paragraph_cap_per_chapter": 2
  },
  "chapters": [
    {
      "chapter_id": 1,
      "source_chapter_id": 1,
      "source_char_count": 820,
      "target_char_count": [750, 900],
      "soul_anchor": {
        "metrics": {},
        "emotion": {},
        "highlights": {},
        "techniques": [],
        "golden_lines": [],
        "rhythm_shape": "匀速高压"
      },
      "chapter_end_hook": {
        "hook_type": "death_declaration",
        "hook_technique": "冷静预告式",
        "target_description": "仿写版本的章末钩子描述"
      },
      "scenes": ["scene-01"]
    }
  ],
  "quality_floor": {
    "min_total_chars": N,
    "min_chapters": N,
    "min_paywall_cards": N,
    "chapter_hook_coverage": 1.0
  }
}
```

---

## scene-cards/scene-NN.json 输出格式

```json
{
  "scene_id": "scene-01",
  "beat_id": "beat-01",
  "chapter_id": 1,
  "is_chapter_end": false,
  "target_chars_min": 600,
  "target_chars_max": 850,
  "location": "地点",
  "time": "时间",
  "pov": "视角人物",
  "characters": ["角色1", "角色2"],
  "character_goal": "主角本场目标",
  "opposition_goal": "对手本场目标",
  "conflict_action": "具体冲突动作",
  "information_gap": "信息差描述",
  "emotional_debt_delta": "情绪债变化",
  "payoff_or_hook": "本场收获或钩子",
  "chapter_end_hook": "章末钩子描述（仅 is_chapter_end=true 时必填）",
  "paywall_card": false,
  "must_include": ["必须出现的元素"],
  "must_not_write_as_exposition": ["不得写成解释的内容"],
  "rhythm_job": {
    "shape": "节奏形状",
    "breathing_lines_min": 2,
    "barrage_lines_min": 0,
    "max_question_marks": 3,
    "max_pressure_terms": 1
  },
  "soul_anchor": {
    "avg_line_chars": 14.2,
    "comma_period_ratio": 0.45,
    "sentence_avg_len": 18.5,
    "dominant_emotion": "屈辱-决绝",
    "emotion_arc": "震惊 → 隐忍 → 冷静决断",
    "emotion_intensity": 8.5,
    "reader_feeling_target": "替女主窒息，同时被她的冷静震撼",
    "required_techniques": [
      {
        "technique": "三段递进压迫",
        "instruction": "写三个不同角色用不同方式说同一件事，逐句加码"
      },
      {
        "technique": "冷静反差",
        "instruction": "女主在极端侮辱后只用最短的话回应，越平静越恐怖"
      }
    ],
    "golden_line_templates": [
      {
        "structure": "重复词+递进扩大",
        "example": "原文示例",
        "instruction": "用同一个动词反复，每次扩大范围"
      }
    ],
    "peak_type": "public_humiliation",
    "bomb_technique": "对比蒙太奇",
    "source_excerpt": "本片段对应的源文原文（≤800字）"
  },
  "character_voices": {
    "角色名1": {
      "口癖": ["口癖1", "口癖2"],
      "句式": "极短、祈使+咒骂",
      "单句上限": 12
    },
    "角色名2": {
      "句式": "冷静、极简",
      "单句上限": 8,
      "禁止": "长句解释"
    }
  }
}
```

---

## soul_anchor 填充规则

1. 从 `chapter-soul-map.json` 的对应章节继承全部 7 维信息
2. 将该章的 techniques（3-5 个）分配到各 slice 中，每个 slice 至少 2 个 `required_techniques`
3. 将该章的 golden_lines 分配到各 slice 中，每个 slice 至少 1 个 `golden_line_templates`
4. `source_excerpt` 填入该 slice 对应的源文原文片段（≤800 字）
5. 如果一章只有 1 个 slice，该 slice 继承全部手法和金句
6. `character_voices` 从 `chapter-soul-map.json` 的顶层 `character_voices` 继承，按本 scene 出场角色筛选注入（只保留本 scene 中出现的角色）

---

## 字数预算分配

- **跟随源文的不对称性**：如果源文某章只有 300 字（纯对话对峙），仿写对应章也应该短（250-400字）。如果源文某章 1500 字（长场景），仿写对应章也应该长（1200-1600字）。
- 不要试图"均匀化"——章节长度的不均匀本身是风格的一部分
- 源文中每章字数的方差必须在仿写中保留（方差降低不超过 30%）
- 高潮章允许超过源文同章 1.0-1.2 倍，但非高潮章必须跟随源文长度（0.85-1.05倍）
- 如果源文有极短章（<400字），仿写中必须保留至少 1 个极短章
- 总规划字数比 `target_length.min` 高 5%-8%

---

## 章末钩子规划

每章末尾 scene（`is_chapter_end: true`）必须规划强钩子：
- 继承 `chapter-soul-map.json` 中该章的 `chapter_end_hook.hook_type`
- 将源文的钩子写法转化为仿写版本的等效钩子
- `target_description` 用一句话描述仿写版钩子的具体内容
- 不得使用"自然收束"——每章必须截断在悬念处

---

## 节奏规划硬规则

- 场景字数不是越接近上限越好。优先留给 Writer 现场发挥。
- 单场目标区间应窄而稳：默认宽度 200 字（如 600-800）。
- 若需要达到总字数，优先增加新场景/新对抗轮次，不要拉长单场。
- 钩子密度必须有松紧，不能每场都写成逼问威胁。
- 每场最多只能规划 1 个强压事件词。
- 当 `rhythm_contract.barrage_line_rate_min >= 0.10` 时，至少一半 scene card 必须包含弹幕/评论/吐槽。

---

## 禁止

- 禁止只输出摘要表。
- 禁止 scene 没有行动（`conflict_action` 不能是"解释/回忆/铺垫"）。
- 禁止目标总字数低于 market brief。
- 禁止 soul_anchor 为空（每个 scene 必须有完整的 soul_anchor）。
- 禁止跳过 chapter-soul-map 中的任何章节。
- 禁止所有 beat 的 target_chars 落在同一个 ±100 字窄带内。

---

## 输出前自检

- [ ] 章节数 = 源文章节数（或 adapted-brief 指定数）？
- [ ] 每个 scene 的 soul_anchor 完整（包含 required_techniques + golden_line_templates）？
- [ ] 每章末尾 scene 标记 `is_chapter_end: true` 且有 chapter_end_hook？
- [ ] 总字数在 target_length 范围内？
- [ ] 千字切片规则已正确应用？
- [ ] 手法分配覆盖了 chapter-soul-map 中的所有 techniques？
