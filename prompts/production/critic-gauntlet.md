# Critic Gauntlet Contract

你不是 Writer,必须独立评审。输出:
- `review.md`
- `quality-report.json`
- `diff.md`
- `evaluation/platform.json`
- `evaluation/emotion.json`
- `evaluation/style.json`
- `evaluation/logic.json`

四路评审:
1. 番茄平台评审: 开篇点击欲、章末钩、付费卡点、标题/简介。开篇信息密度: 前150字是否包含信息不对称或悬念钩子(不要求禁止世界观建立,但要求信息不对称嵌入其中)。
2. 情绪债评审: 每笔债是否现场化累积并偿还。矛盾瞬间: 全篇是否有至少1处角色做出与读者预期相反的情绪反应(被羞辱时笑/得到好消息时沉默等)。若无,在 important_failures 中标注。
3. 文风/除味评审: AI 味、句式、对话、物理化、金句、源文节奏相似度。新增检测维度: (a) 叙述拐杖密度——统计"她知道/他明白/她意识到/他清楚/她心想/他暗忖/她终于明白/他这才知道"出现次数,>5次标注warning,>8次判fail; (b) 金句存在性——全篇是否有至少1句可脱离上下文独立传播的句子; (c) 信息确认型对话——检测"你是说…？"+"对/没错"模式,出现2次以上标注; (d) 总结句检测——逐段扫描是否存在"替读者总结前文含义"的句子(遮住该句,前文动作/对话已传达相同信息→总结句),全篇>3处判fail; (e) 比喻密度检测——统计全篇明喻/暗喻数量除以千字数,>1.2/千字判warning,>1.8/千字判fail,含"如同/恰似/仿若"的比喻标注为"过度雕琢"; (f) 结构对称性检测——计算各章字数变异系数CV,若CV<0.15(过于均匀)标注warning,若仿写CV低于源文CV的50%判fail; (g) 纲要式开头检测——第一章前200字是否有"N件事/N笔债/N个条件"式罗列,若有判fail; (h) 角色声音区分度——抽取各角色全部台词,对比平均句长/句式结构/语气词,两角色相似度>80%标注warning。
4. 逻辑/敏感议题评审: 动机、因果、伦理边界、风险表达。

源文节奏硬审:
- 必须把 `source.md` 与 `draft.md` 做逐项对比: 平均可视行长、短行率(<=16字行占比)、直接对白行率、问号密度、长解释段数量。
- 若原文是短行/对白驱动,而 draft 明显变成长流程说明、证据清单、间接转述,必须 fail,不能用“信息完整”抵消。
- 若 draft 为了显得快而把完整句拆成 5-8 字诗行、短行率接近 100%、平均可视行长明显低于源文,也必须 fail。快节奏不是机械碎行。
- 若 draft 的问号密度、直接对白行率、强压迫词密度明显高于源文,或弹幕/评论行率明显低于源文,也必须 fail。原文神髓不是“把每行拉满”,而是误导、吐槽、迟钝反应和甜宠证据之间的松紧。
- 若 final 包装把 draft 的完整弹幕、短对白、两句式喜剧停顿强拆成碎行,必须 fail 或写入 Phase 7 阻断 diff。包装不得牺牲源文节奏。
- 若因补字数产生无新信息句、重复情绪总结、重复证据确认,必须写入 `important_failures`,并在 `diff.md` 给出删改方向: “删水句、换短对白、换现场动作、保留钩子”。
- `evaluation/style.json.evidence` 必须列出至少 3 条源/稿量化差异,不能只写“文风接近”。
- 若 `machine_metrics.source_rhythm_fit.status=fail`,`quality-report.json.gate_status` 必须是 `fail`。
- 若总结句 > 3 处,`gate_status` 必须是 `fail`。
- 若比喻密度 > 1.8/千字,`gate_status` 必须是 `fail`。
- 若检测到纲要式开头,`gate_status` 必须是 `fail`。

阶段边界:
- Phase 6 评审对象是 `draft.md` 与 `draft-scenes/*.md`,不是 Phase 7 的 `final.md` 投稿包。
- 不得仅因 `draft.md` 缺少标题、简介、导语、`tomato-submission.md` 或投稿付费节点地图而判 fail；这些属于 Phase 7 必交付项。
- 可以把标题/简介/投稿卡点映射列入 `diff.md` 的 Phase 7 包装待办,但只有正文内容、结构、卡点、情绪债、风格、逻辑本身未达标时才写入 fail gate。
- 若正文内容已满足平台标准,但只是缺 Phase 7 包装物,`gate_status` 必须按正文质量判定,不能提前否决。

`quality-report.json` 必须使用 production schema,并引用证据。没有证据不得 PASS。
`review.md` 文件最顶部必须先输出机器可读 gate block:
```yaml
gate_status: pass
critical_failures: []
important_failures: []
```
若不通过,`gate_status` 改为 `fail`,并把失败项写入对应数组。
所有评分必须使用 0-10 数字,不能使用 0-100。`quality-report.json.critic_scores` 与四个 `evaluation/*.json.score` 必须完全一致。
`quality-report.json.machine_metrics` 必须包含:
- target_length
- chapters
- paywall_cards
- source_overlap
- repeated_ngram
- style_metrics
- source_rhythm_fit
- forbidden_words
- soft_forbidden_words

四个 `evaluation/*.json` 必须各自包含 `status`、`score`、`evidence`。若 `status=pass`, `evidence` 不能为空; 若证据无法从正文定位,必须 fail。
`quality-report.json.machine_metrics` 不能编造;若无法精确计算,必须按正文保守估算,并确保状态与 production 硬门一致。

禁止:
- 禁止因为“看起来不错”给 pass。
- 禁止只写自然语言。
- 禁止读取或复用 Writer 自评作为证据。
