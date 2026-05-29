# V4 人工校准清单

```yaml
slug: apocalypse_exile_revenge
genre: apocalypse_heroine
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 《末世让我滚出基地后，所有人都死了》.txt
- **word_count**: 11739
- **mechanisms**: [M7, M6, M8]
- **dominant_s爽点(machine)**: 降维打击
- **tomato_fit_score(machine)**: 8.2

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看被基地当工具又驱逐的大女主，跌入另一套末世规则后从净化体跃迁为辐射本体，让旧基地因抛弃她而覆灭。 |
| emotional_debt_type | 见 corpus/_index.json | 放逐背叛债 / 工具弃置债 |
| dominant_s爽点 | 降维打击 | 降维打击 |
| antagonist_violation | 见 corpus/_index.json | 基地和江岚只把主角当屏障工具，享受她的价值却在风险来临时驱逐她。 |
| protagonist_stance | 见 corpus/_index.json | 冷硬、强大、少解释、末世神明感 |
| payoff_pattern | 见 corpus/_index.json | 主角从人类秩序的弱者跃迁为异兽/辐射秩序的王，旧基地在失去她后按自己选择崩塌，结尾保留孤独代价。 |
| tomato_fit_score | 8.2 | 8.6 |

## 人工校准 Checklist

- [x] 读完 `dissection.md`,确认机器 reader_promise 是否真的对应原 case 的读者承诺。
- [x] 对照 `analysis/soul-contract.md`,确认情绪债不是泛化模板,而是该 case 特有的债。
- [x] 对照 M1-M8,确认 dominant_s爽点 是主导爽点而非列表第一个机制。
- [x] 检查 antagonist_violation 是否具体到“违反了什么读者道德底线”。
- [x] 检查 protagonist_stance 是否能指导改编写手复刻主角姿态。
- [x] 检查 payoff_pattern 是否描述了清算动作,而不是泛泛说“反派被惩罚”。
- [x] 检查 tomato_fit_score 是否与标题点击欲、首章留存、卡点密度相符。
- [x] 写下至少 2 条“神髓禁改项”和 2 条“可替换项”。

## 校准结论

### 调整后的爆款基因

reader_promise: 看被基地当工具又驱逐的大女主，跌入另一套末世规则后从净化体跃迁为辐射本体，让旧基地因抛弃她而覆灭。

emotional_debt_type: 放逐背叛债 / 工具弃置债

dominant_s爽点: 降维打击

antagonist_violation: 基地和江岚只把主角当屏障工具，享受她的价值却在风险来临时驱逐她。

protagonist_stance: 冷硬、强大、少解释、末世神明感

payoff_pattern: 主角从人类秩序的弱者跃迁为异兽/辐射秩序的王，旧基地在失去她后按自己选择崩塌，结尾保留孤独代价。

tomato_fit_score: 8.6

### 神髓禁改项

1. 必须有两套规则：基地人类秩序与辐射/异兽秩序。
2. 跃迁句“我不再净化辐射，我就是辐射本身”式结构不可丢。
3. 驱逐动作要具体，不能只靠口头排挤。
4. 结尾必须有“拥有世界也失去世界”的道德模糊代价。

### 可替换项

1. 净化体可替换为治愈者、供能核心、预言者、屏障源。
2. 基地可替换为舰队、避难城、实验区。
3. 辐射/异兽规则可替换为虫族、深海、机械、污染源规则。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
