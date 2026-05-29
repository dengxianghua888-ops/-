# Final Packager Contract

只有 phase6 质量门通过后才能执行。输出:
- `final.md`
- `craft-notes.md`
- `tomato-submission.md`
- `final-chapters/_chapters-map.md`
- `final-chapters/chNN.md`
- `story.yaml`

要求:
- 根据 `diff.md` 精修,不得缩短到目标长度以下。
- 精修的首要任务是提速: 删除无新信息的补字句,把间接转述改回直接短对白,把流程说明改成现场动作或证据翻转。
- 必须保持或修复 `source_rhythm_fit`: 平均可视行长、短行率、直接对白行率、问号密度要贴近 `analysis/style-dna.md` / `quality-report.json` 的源文节奏要求。
- 直接投稿的一行一句不是一行半句,也不是把所有标点都拆开。不要把“离婚两个字落在桌上时，我包底还压着早孕单。”拆成两行；不要把 `【等等？离婚协议里写孩子？】` 拆成三行。
- `final.md` 必须是直接投稿版结构:
  1. 第 1 行为 `# 标题`。
  2. 标题后、第一章前必须有 2-5 段开篇导语,第一段以 `导语：` 开头,总长度不少于 60 个非空白字符。
  3. 导语要直接抛出主角处境、极端冲突、反击承诺,不能写成创作说明。
  4. 正文必须是移动端短段落,但不要机械拆句；优先保留 `draft.md` 的源文式可视行节奏。
  5. 允许两个极短关联句留在同一行,允许完整弹幕 `【...】` 保持一行,不得把弹幕或引号内句子从中间拆开。
  6. 直接对白必须保留中文引号和说话对象,不要为了“一句一段”改成旁白转述。
  7. 正文不得出现 `【付费节点】`、`付费节点`、`付费卡点`、`paywall` 等内部标记。
- 章节标题必须使用二级标题 `## 第N章`,不能使用一级标题 `# 第N章`;整篇 final.md 只有总标题可以用一级标题。
- 默认保持 `draft-scenes/scene-*.md` 的数量和顺序拆章,除非单章长度会越界。
- 切章 500-1200 字,每章末有明确钩子；不得为了整合提交包把多个 scene 合并成超长章节。
- 切章时宁可多保留短章钩子,不要把短章合并成长章导致节奏变慢。
- 付费节点必须自然落在章末或强悬念句上,以“证据半露 / 真相卡住 / 反击刚启动”的截断制造付费拉力。
- 投稿包必须包含标题 A/B/C、90-120 字简介、标签、前三章钩子说明、`付费节点地图（直接投稿版）`。
- `付费节点地图（直接投稿版）` 必须用 Markdown 表格列出至少 `ceil(正文字符数/3500)` 个节点,正文不显式标注付费点。
- `story.yaml` 顶层必须写入 `pipeline_mode: production` 和 `status: final`,并写入 `runner_policy.external_allowed`, provider/model/source 审计字段。
- `quality_gate` 必须与 `quality-report.json` 一致；若 final.md 或 final-chapters 改变了字数、章节数、钩子覆盖率,必须同步更新 `quality-report.json.machine_metrics` 后再输出。
- `quality-report.json.critic_scores` 与四个 `evaluation/*.json.score` 必须维持 0-10 分制,不得改回 0-100。
- `quality-report.json.machine_metrics.direct_submission` 必须包含开篇导语、源文式移动端短段落、付费节点地图、正文无内部付费标签四项校验结果。
- 章节必须全部 500-1200 字,`final-chapters/_chapters-map.md` 每一章都要有非空钩子；表格最后一列必须是章末钩子文本,不能把“常规悬念/自然卡点”放在最后一列。
