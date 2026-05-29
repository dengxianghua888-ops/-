# Style DNA：文体基因与机器可读指标

## 一、整体叙事风格

原文是典型番茄女频短篇爽文语体：第一人称、强事件驱动、短句密集、情绪直接但不长篇抒情。核心优势在于“女主行动快、证据节点密、前夫悔恨长”。

叙述不是纯复仇文，而是“受伤—止损—重建—反转—火葬场”的 U 型抬升结构。

## 二、机器可读指标

> 注：根据源文正文估算，主要用于后续仿写校准。

```json
{
  "estimated_source_length_chars": 24800,
  "estimated_paragraph_count": 290,
  "average_paragraph_length_chars": 85,
  "average_sentence_length_chars": 22,
  "dialogue_ratio": 0.31,
  "question_mark_density_per_1000_chars": 2.6,
  "exclamation_density_per_1000_chars": 1.9,
  "golden_sentence_density_per_1000_chars": 1.4,
  "first_person_density": "high",
  "flashback_ratio": 0.38,
  "present_action_ratio": 0.42,
  "retrospective_summary_ratio": 0.20,
  "emotion_word_density": "medium",
  "concrete_action_density": "high",
  "evidence_prop_density": "high"
}
```

## 三、句法特征

### 1. 短句压迫开局

原文开头连续短句：

> “综艺里，我和姐姐都失足落水。”  
> “而我的老公霍霆，不假思索地跳入水里救起了姐姐。”  
> “他心疼又焦急地抱着人头也不回地走了。”

特点：

- 每句只推进一个事实。
- 不解释人物关系。
- 先给结果，再补因果。
- 情绪词少，事实冲击强。

仿写规则：

- 首 300 字平均句长控制在 18-24 字。
- 每段 1-3 句。
- 不用“曾经”“命运”“绝望”等抽象开头。

### 2. 女主冷静台词

代表句：

> “嗯，签吧！”  
> “不用了。”  
> “离婚了，就是离婚了，不是亲人，更没法当朋友。”  
> “你们什么都没有又和我有什么关系呢？”

特点：

- 台词短。
- 不解释。
- 不请求。
- 高频使用事实判断：“离婚了”“不用了”“没关系”。

仿写规则：

- 女主关键拒绝台词 ≤18 字。
- 情绪越强，台词越短。
- 避免“你知道我有多痛吗”式控诉。

### 3. 前夫后悔段长句增多

后期霍霆视角里，句子变长，回忆密度变高：

> “脑子里浮现一个影子，温柔地给他按摩腿，牵着手看电影，挖冰激凌递到他嘴边，还有每天等着他下班的身影。”

特点：

- 用并列动作堆积悔恨。
- 不是直接说“他很后悔”，而是让记忆反复攻击他。
- 身体反应与回忆交替。

仿写规则：

- 前夫悔恨段可使用 35-55 字长句。
- 每段至少一个身体反应：胸闷、手抖、腿疼、喘不上气、眼红。
- 回忆必须是前文出现过的具体动作。

## 四、段落节奏

### 段落长度分布

- 高冲突段：10-40 字，短段密集。
- 回忆解释段：80-160 字，中长段。
- 舆论爆料段：50-120 字，评论与证据交替。
- 火葬场段：70-180 字，内心与回忆交织。

### 节奏模型

```text
强冲突短段 → 回忆补因 → 新冲突短段 → 证据释放 → 评论发酵 → 身份升维 → 前夫崩塌
```

## 五、对话风格

### 女主

关键词：平静、直接、事实化、边界明确。

示例：

> “霍霆，如果没什么事我挂了！”  
> “算了吧，霍霆，以后不要给我打电话了。”  
> “我不喜欢你了，不会和你复婚的。”

台词 DNA：

```json
{
  "heroine_dialogue_style": {
    "sentence_length": "short",
    "emotion_level": "controlled",
    "dominant_function": ["cut_boundary", "state_fact", "refuse"],
    "avoid": ["pleading", "long_accusation", "self_proof"]
  }
}
```

### 霍霆

关键词：高位误判、迟来脆弱、解释、自我合理化、崩溃。

示例：

> “琳琳不会水，所以我才先救她，这你都要吃醋？”  
> “思思，我想你了！”  
> “我以为你只是赌气和我离婚……”

台词 DNA：

```json
{
  "ex_husband_dialogue_style": {
    "early_stage": ["accusatory", "condescending", "misreading"],
    "middle_stage": ["probing", "dependent", "nostalgic"],
    "late_stage": ["pleading", "self_humbling", "regretful"],
    "core_flaw": "把女主的决绝误判为赌气"
  }
}
```

### 沈琳琳

关键词：撒娇、柔弱、人设表演、背后粗鄙。

前台：

> “对不起妹妹，我是太开心了。”

后台：

> “都是我挑剩下的。”  
> “他们宠我，却对自己的亲生女儿不好，你说他们蠢不蠢。”

台词 DNA：

```json
{
  "false_sister_dialogue_style": {
    "public_mask": ["soft", "apologetic", "victim_like"],
    "private_truth": ["vulgar", "mocking", "classist"],
    "reversal_method": "public_private_contrast_video"
  }
}
```

### 博斯远

关键词：看见、尊重、克制、价值识别。

示例：

> “如果分手了，肯定是他对不起你。”  
> “都过去了，你是很了不起的人，失去你，是他们的损失。”

台词 DNA：

```json
{
  "new_male_lead_dialogue_style": {
    "function": ["recognize_value", "provide_safe_space", "contrast_ex_husband"],
    "tone": "gentle_but_clear",
    "avoid": ["霸道替她决定", "只负责吃醋", "过早表白"]
  }
}
```

## 六、情绪承载方式

### 1. 不用长篇哭诉，用动作承载

- “把离婚协议书交给霍霆”
- “挂了电话拉黑删除一条龙”
- “打开手机买了去国外的机票”
- “登录微博，把聊天记录发到上面”

这类动作让女主显得清醒，不沉溺受害者叙事。

### 2. 用物品承载婚姻价值

- 红宝石袖口
- 深蓝格子休闲外套
- 按摩手法
- 小蛋糕
- 冰激凌
- 书房照片
- 落水视频

物品功能：

```json
{
  "props": [
    {
      "name": "红宝石袖口",
      "function": "离婚后霍霆生活失序"
    },
    {
      "name": "按摩手法",
      "function": "女主长期照料价值"
    },
    {
      "name": "落水视频",
      "function": "霍霆反复受刑的悔恨载体"
    },
    {
      "name": "聊天记录",
      "function": "舆论反杀证据"
    },
    {
      "name": "耶鲁通知书",
      "function": "人生升维标志"
    }
  ]
}
```

### 3. 用第三方证明女主价值

原文很少让女主自夸，而是通过他人证明：

- 刘姐支持她、骂渣男绿茶。
- 博斯远看见她付出。
- 京大学姐证明她论文与项目能力。
- 导师认可她在耶鲁的存在。
- 网友从质疑转为震惊。

仿写规则：女主价值不要靠自述，靠第三方证言、证据、成果。

## 七、金句密度与金句类型

### 代表金句

> “真好，我可以开始为自己而活了。”  
> “离婚了，就是离婚了，不是亲人，更没法当朋友。”  
> “你们什么都没有又和我有什么关系呢？”  
> “失去你，是他们的损失。”  
> “我错把鱼目当珍珠，永远地失去了她。”  
> “爱能让人生出骨血，霍霆却亲手掐断了它。”

### 金句类型

| 类型 | 功能 | 示例 |
|---|---|---|
| 边界金句 | 女主断联 | “离婚了，就是离婚了。” |
| 独美金句 | 新人生开启 | “为自己而活。” |
| 识别金句 | 新男主补偿 | “失去你，是他们的损失。” |
| 悔恨金句 | 前夫火葬场 | “错把鱼目当珍珠。” |
| 主题金句 | 爱与失去 | “爱能让人生出骨血……” |

## 八、AI 味规避规则

必须避免：

- “命运的齿轮开始转动”
- “我在绝望中重生”
- “那一刻，我终于明白”
- “他不知道的是”
- “属于我的复仇才刚刚开始”
- 大段解释女主有多痛

应该使用：

- 具体动作：递协议、拉黑、买机票、发证据。
- 具体物品：袖口、外套、视频、通知书。
- 具体证人：学姐、保姆、网友、刘姐。
- 具体身体：沉入湖底、眼眶通红、手抖、腿疼、喘不上气。

## 九、后续仿写硬指标

```json
{
  "target_style_constraints": {
    "opening_300_chars": {
      "average_sentence_length_chars": "18-24",
      "must_include": ["生死事件", "丈夫选择别人", "女主冷静离婚"],
      "forbid": ["长篇背景", "自怜", "解释姐姐身世"]
    },
    "dialogue_ratio": "0.28-0.35",
    "question_mark_density_per_1000_chars": "2-4",
    "golden_sentence_density_per_1000_chars": "1-2",
    "micro_hook_interval_chars": "800-1200",
    "payoff_interval_chars": "2500-3500",
    "heroine_core_tone": "冷静、边界、行动",
    "ex_husband_core_tone": "误判、依赖、崩溃",
    "evidence_release_style": "分批、第三方、硬证据"
  }
}
```
