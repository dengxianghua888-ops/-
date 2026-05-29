# V4 人工校准清单

```yaml
slug: dead_autopsy_pregnant
genre: ancient_BE
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 《我死后，老公亲手解剖了我的尸体，却没发现我怀孕了》.txt
- **word_count**: 21182
- **mechanisms**: [M4, M5, M1]
- **dominant_s爽点(machine)**: 灵魂线视角
- **tomato_fit_score(machine)**: 8.2

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看亡妻灵魂无力旁观爱人以“绝对理性”亲手解剖自己，并在怀孕真相爆开时让理性信条反噬成终身惩罚。 |
| emotional_debt_type | 见 corpus/_index.json | 死后旁观信息差债 / 理性错杀债 |
| dominant_s爽点 | 灵魂线视角 | 灵魂线视角 |
| antagonist_violation | 见 corpus/_index.json | 江川把“公正”和“理性”放在妻子生命与亲密信任之上，亲手把爱人的身体变成证据对象。 |
| protagonist_stance | 见 corpus/_index.json | 死后无力旁观、哀而不求、冷静自述 |
| payoff_pattern | 见 corpus/_index.json | 怀孕信息差在解剖场景中爆裂，江川的理性信条变成亲手毁掉妻儿的罪证，悔悟不可逆。 |
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

reader_promise: 看亡妻灵魂无力旁观爱人以“绝对理性”亲手解剖自己，并在怀孕真相爆开时让理性信条反噬成终身惩罚。

emotional_debt_type: 死后旁观信息差债 / 理性错杀债

dominant_s爽点: 灵魂线视角

antagonist_violation: 江川把“公正”和“理性”放在妻子生命与亲密信任之上，亲手把爱人的身体变成证据对象。

protagonist_stance: 死后无力旁观、哀而不求、冷静自述

payoff_pattern: 怀孕信息差在解剖场景中爆裂，江川的理性信条变成亲手毁掉妻儿的罪证，悔悟不可逆。

tomato_fit_score: 8.6

### 神髓禁改项

1. 死亡必须在前20%触发，灵魂只能旁观不能干预。
2. 怀孕/子宫信息差必须后置引爆，读者要提前背负“他要切到了”的焦虑。
3. 爱人之手变解剖刀的温度反转必须具体可触。
4. 手术灯、白布、器官隐喻等冷意象不可丢。

### 可替换项

1. 法医可替换为仵作、医生、鉴定师等“专业理性之手”。
2. 怀孕可替换为足以摧毁关系信条的隐藏生命/遗物/证据。
3. 现代解剖室可替换为古代验尸房、医院手术室或事故鉴定现场。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
