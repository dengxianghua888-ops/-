# StoryForge 经验笔记(人类入口, V3)

> **V3 分工**:本文件仅保留**人类可读的摘要洞察与战略笔记**;所有结构化的跨案例数据(违禁词学习/机制成败/Style DNA 统计)走 `context/*.json`,由 finalizer Step 5 自动写入。
>
> 不要在本文件里堆原始数据表格——那是 `context/` 的职责。本文件只记"**阅读者需要秒懂的洞察**"。

## 索引

- 结构化数据:
  - `context/forbidden-words-learned.json` — 按 genre 学习到的新违禁词
  - `context/mechanism-playbook.json` — M1-M8 各机制成败案例库
  - `context/style-dna-stats.json` — 各 genre 的文风定量均值/方差
- 批量刷新结构化数据:
  - `python3 scripts/update-corpus-index.py`(索引)
  - `python3 scripts/aggregate-style-stats.py`(统计)

---

## 战略洞察(逐项迭代时往下加)

### 2026-04-20 · V3 启动观察

**题材外推风险最大的是 ancient_BE**——现代反转/家庭伦理/urban_sweet_ceo 的文风差异较小,共用基线模板即可;但 `ancient_BE` 的意象密度/破句节奏/半文半白基线独立,**必须按 genre 分开训练,否则 AI 会把古言写成白话小说**。

**反转机制的改编风险集中在 M3(因果回旋反讽)**——它的命脉是"首尾金句回敬",而 AI 改编时最易把结尾金句写成"新创作"而非"原句复用"。V3 在 finalizer.md Step 2g 显式加了机制收尾验证,强制校对开头伏笔+结尾回敬。

**番茄特化不是可选**——平台的章节硬约束(500-800 字)+ 付费卡点(每 3000 字一处)和短篇"一气呵成"的创作本能冲突。V3 把它做成 finalizer Step 6 的后处理,而非 writer 阶段的约束,避免干扰创作主流程。

---

## 常见问题与解法(案例驱动,简短)

- **Q: 古言改编里混入现代词(手机/公司)如何防?**
  A: V3 的 `workspace.yaml::genre_profiles.ancient_BE.extra_forbidden` 硬编码了现代词清单,editor 的 C4 4d 会扫描。新发现的个案加到 `context/forbidden-words-learned.json` 的 `ancient_BE` 数组,出现 ≥3 次升级到 `prompts/patterns/forbidden-and-preferred.md`。

- **Q: M1 死环反杀的"固化载体"怎么换皮?**
  A: 看 `context/mechanism-playbook.json` 的 M1.success_cases。已验证的载体替换:海关完税单 → 考研成绩确认书 → (可扩展)工程验收单/医疗诊断书/资产评估报告。只要是"盖公章+可被反向使用"的第三方背书文书即可。

---

## 质量趋势(每次跑批后填)

| 项目 | genre | 机制 | C1 | C2 | C3 | C4 | C5 | I4 | 结论 |
|------|-------|------|-----|-----|-----|-----|-----|-----|------|
| hermes_bag | modern_reversal | M1+M3 | 95% | 92% | 2% | 0 违禁 | ✅ | ±3% | 教科书级 |
| (待填充) | | | | | | | | | |
