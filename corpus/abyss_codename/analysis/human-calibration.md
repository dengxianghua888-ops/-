# V4 人工校准清单

```yaml
slug: abyss_codename
genre: apocalypse_heroine
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 《她代号深渊》.txt
- **word_count**: 21089
- **mechanisms**: [M2, M6, M7]
- **dominant_s爽点(machine)**: 降维打击
- **tomato_fit_score(machine)**: 8.0

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看22岁伪装转学生一步步揭开“代号深渊”的真实身份，用专业侧写能力在校园与犯罪学两套规则间降维破局。 |
| emotional_debt_type | 见 corpus/_index.json | 身份低估债 / 认知错位债 |
| dominant_s爽点 | 降维打击 | 身份反差爆发 |
| antagonist_violation | 见 corpus/_index.json | 凶手、警方和校园环境都误判主角年龄、性别与能力，把神级侧写师当普通学生。 |
| protagonist_stance | 见 corpus/_index.json | 冷硬、克制、专业推理优先、无恋爱依附 |
| payoff_pattern | 见 corpus/_index.json | 转学生、卧底、侧写专家三层身份递进揭开，主角用可量化履历和心理博弈碾压对手，第二个“画师”留下续作钩子。 |
| tomato_fit_score | 8.0 | 8.2 |

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

reader_promise: 看22岁伪装转学生一步步揭开“代号深渊”的真实身份，用专业侧写能力在校园与犯罪学两套规则间降维破局。

emotional_debt_type: 身份低估债 / 认知错位债

dominant_s爽点: 身份反差爆发

antagonist_violation: 凶手、警方和校园环境都误判主角年龄、性别与能力，把神级侧写师当普通学生。

protagonist_stance: 冷硬、克制、专业推理优先、无恋爱依附

payoff_pattern: 转学生、卧底、侧写专家三层身份递进揭开，主角用可量化履历和心理博弈碾压对手，第二个“画师”留下续作钩子。

tomato_fit_score: 8.2

### 神髓禁改项

1. 开头必须高密度叠加年龄、性别、代号、履历等身份标签。
2. “普通转学生”与“代号深渊”的双身份差必须贯穿。
3. 能力要量化，如侦破案件数、年限、代号战绩。
4. 开放式第二凶手/画师钩子不可写成烂尾。

### 可替换项

1. 校园可替换为医院、警校、企业、训练营。
2. 侧写能力可替换为法医、黑客、谈判、战术推演。
3. 代号深渊可替换为任何强标签暗号。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
