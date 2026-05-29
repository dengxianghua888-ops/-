# V4 人工校准清单

```yaml
slug: husband_drug_mom_revenge
genre: family_ethics
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 老公给我妈下药后，我杀疯了.txt
- **word_count**: 8845
- **mechanisms**: [M3, M1, M5]
- **dominant_s爽点(machine)**: 因果回旋反讽
- **tomato_fit_score(machine)**: 8.7

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看丈夫为讨好婆婆给岳母下药后，妻子把同一套药、话术和证据链原样回敬，让愚孝家庭付出刑事与伦理双重代价。 |
| emotional_debt_type | 见 corpus/_index.json | 伤母背叛债 / 愚孝压迫债 |
| dominant_s爽点 | 因果回旋反讽 | 因果回旋反讽 |
| antagonist_violation | 见 corpus/_index.json | 丈夫和婆婆借家庭伦理伤害女主母亲，还试图用“都是一家人”消解罪行。 |
| protagonist_stance | 见 corpus/_index.json | 受伤后冷硬、不哭求、不和解、证据型复仇 |
| payoff_pattern | 见 corpus/_index.json | 下药动作镜像回旋，诊断书、住院记录和转账记录形成死环，结尾明确切断家庭关系。 |
| tomato_fit_score | 8.7 | 8.5 |

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

reader_promise: 看丈夫为讨好婆婆给岳母下药后，妻子把同一套药、话术和证据链原样回敬，让愚孝家庭付出刑事与伦理双重代价。

emotional_debt_type: 伤母背叛债 / 愚孝压迫债

dominant_s爽点: 因果回旋反讽

antagonist_violation: 丈夫和婆婆借家庭伦理伤害女主母亲，还试图用“都是一家人”消解罪行。

protagonist_stance: 受伤后冷硬、不哭求、不和解、证据型复仇

payoff_pattern: 下药动作镜像回旋，诊断书、住院记录和转账记录形成死环，结尾明确切断家庭关系。

tomato_fit_score: 8.5

### 神髓禁改项

1. 下药动作必须具体可信，并在后文镜像回旋。
2. 母亲作为沉默受害者的重量不可削弱。
3. 不得出现和稀泥式和解。
4. 诊断书/银行流水/病房记录等固化证据不可少。

### 可替换项

1. 药可替换为保健品、过敏源、手术费挪用、护理事故。
2. 婆媳/女婿结构可替换为父子、兄妹、再婚家庭。
3. 饭桌/病房/家门口三类家庭场景可替换但密度要保留。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
