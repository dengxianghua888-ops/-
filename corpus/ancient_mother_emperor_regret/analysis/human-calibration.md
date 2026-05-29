# V4 人工校准清单

```yaml
slug: ancient_mother_emperor_regret
genre: ancient_BE
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 《娘亲脱离世界后，父皇悔疯了》.txt
- **word_count**: 14122
- **mechanisms**: [M5, M4, M8, M6]
- **dominant_s爽点(machine)**: 灵魂线视角
- **tomato_fit_score(machine)**: 8.0

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看被好孕系统工具化的娘亲在“不闹了”的平静中离场，迫使父皇在绝嗣真相和不可逆失去里悔疯。 |
| emotional_debt_type | 见 corpus/_index.json | 生育工具化债 / 错付冷待债 |
| dominant_s爽点 | 灵魂线视角 | 温度反转清算 |
| antagonist_violation | 见 corpus/_index.json | 父皇把娘亲的生育、忍耐和爱都当作理所当然，纵容贵妃伤害孩子，还把系统功劳误认成自己的皇权。 |
| protagonist_stance | 见 corpus/_index.json | 娘亲决绝抽身，女儿清醒旁观、冷静记账 |
| payoff_pattern | 见 corpus/_index.json | 三日倒计时和绝嗣真相揭开后，父皇的悔悟只剩惩罚功能，娘亲不可追回。 |
| tomato_fit_score | 8.0 | 8.4 |

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

reader_promise: 看被好孕系统工具化的娘亲在“不闹了”的平静中离场，迫使父皇在绝嗣真相和不可逆失去里悔疯。

emotional_debt_type: 生育工具化债 / 错付冷待债

dominant_s爽点: 温度反转清算

antagonist_violation: 父皇把娘亲的生育、忍耐和爱都当作理所当然，纵容贵妃伤害孩子，还把系统功劳误认成自己的皇权。

protagonist_stance: 娘亲决绝抽身，女儿清醒旁观、冷静记账

payoff_pattern: 三日倒计时和绝嗣真相揭开后，父皇的悔悟只剩惩罚功能，娘亲不可追回。

tomato_fit_score: 8.4

### 神髓禁改项

1. “她突然不闹了”的违和开场必须保留。
2. 死亡/脱离世界倒计时必须以数字推进，不能只写抽象心死。
3. 父皇绝嗣真相必须成为悔疯核心，而不只是迟来的爱情。
4. 女儿视角必须保持旁观距离，不能改成娘亲直接控诉。

### 可替换项

1. 系统任务可替换为诅咒、契约、药引、神谕。
2. 父皇可替换为王爷、宗主、将军等权力型男主。
3. 九子/绝嗣可替换为血脉、功法、家族继承等不可逆价值。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
