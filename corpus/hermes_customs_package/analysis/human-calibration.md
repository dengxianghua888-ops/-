# V4 人工校准清单

```yaml
slug: hermes_customs_package
genre: modern_reversal
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 海关说我的破包是爱马仕，那就按爱马仕赔吧.txt
- **word_count**: 10094
- **mechanisms**: [M1, M3]
- **dominant_s爽点(machine)**: 死环反杀
- **tomato_fit_score(machine)**: 8.7

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看义乌小厂老板被AI和海关公章逼到倾家荡产后，用对方盖章确认的“三千万爱马仕”构造无解死环，把腐败查验链条送进牢里。 |
| emotional_debt_type | 见 corpus/_index.json | 规则压迫债 / 小微企业生存债 |
| dominant_s爽点 | 死环反杀 | 死环反杀 |
| antagonist_violation | 见 corpus/_index.json | 孙大庆滥用海关权力、AI系统和公章，把普通小老板的生存线当作敲诈筹码。 |
| protagonist_stance | 见 corpus/_index.json | 清醒隐忍、证据型反击、不靠暴力只靠逻辑 |
| payoff_pattern | 见 corpus/_index.json | 完税单从压迫凭证变成反杀凭证，承认破包即伪造公文，坚持真包即监守自盗，结尾用“电脑怎么报”金句回旋。 |
| tomato_fit_score | 8.7 | 9.0 |

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

reader_promise: 看义乌小厂老板被AI和海关公章逼到倾家荡产后，用对方盖章确认的“三千万爱马仕”构造无解死环，把腐败查验链条送进牢里。

emotional_debt_type: 规则压迫债 / 小微企业生存债

dominant_s爽点: 死环反杀

antagonist_violation: 孙大庆滥用海关权力、AI系统和公章，把普通小老板的生存线当作敲诈筹码。

protagonist_stance: 清醒隐忍、证据型反击、不靠暴力只靠逻辑

payoff_pattern: 完税单从压迫凭证变成反杀凭证，承认破包即伪造公文，坚持真包即监守自盗，结尾用“电脑怎么报”金句回旋。

tomato_fit_score: 9.0

### 神髓禁改项

1. 正式完税单/公章必须写明高估值，这是死环触发器。
2. “电脑怎么报”式规则句必须前后镜像。
3. 前半必须让主角真实交钱/抵押，情绪债要有代价。
4. 结尾工厂爆红要完成“真就值三千万”的价值回甘。

### 可替换项

1. 海关可替换为学校、医院、拆迁办、审计、平台仲裁。
2. 完税单可替换为成绩确认书、诊断书、验收单、处罚决定书。
3. 皮包可替换为任何低价物被官方错误高估的载体。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
