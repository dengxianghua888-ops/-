# V4 人工校准清单

```yaml
slug: sister_rebirth_my_death
genre: family_ethics
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 姐姐新生之时，是我的死亡之日.txt
- **word_count**: 10661
- **mechanisms**: [M4, M5, M3]
- **dominant_s爽点(machine)**: 因果回旋反讽
- **tomato_fit_score(machine)**: 8.1

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看妹妹被父母借预言弹幕牺牲后，以灵魂视角旁观全家“救姐姐”的仪式如何变成伦理反噬，最终用转世胎记留下安静却锋利的追问。 |
| emotional_debt_type | 见 corpus/_index.json | 牺牲替罪债 / 预言绑架债 |
| dominant_s爽点 | 因果回旋反讽 | 灵魂线视角 |
| antagonist_violation | 见 corpus/_index.json | 父母把预言当作伤害小女儿的正当理由，用“你懂点事”的温柔话术完成残忍牺牲。 |
| protagonist_stance | 见 corpus/_index.json | 死后无力旁观、不撒泼控诉、用冷静反问保留不甘 |
| payoff_pattern | 见 corpus/_index.json | 姐姐拒绝以妹妹死亡换来的救法，父母的预言逻辑自我崩塌，转世胎记暗示妹妹离开原家庭重获可能。 |
| tomato_fit_score | 8.1 | 8.3 |

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

reader_promise: 看妹妹被父母借预言弹幕牺牲后，以灵魂视角旁观全家“救姐姐”的仪式如何变成伦理反噬，最终用转世胎记留下安静却锋利的追问。

emotional_debt_type: 牺牲替罪债 / 预言绑架债

dominant_s爽点: 灵魂线视角

antagonist_violation: 父母把预言当作伤害小女儿的正当理由，用“你懂点事”的温柔话术完成残忍牺牲。

protagonist_stance: 死后无力旁观、不撒泼控诉、用冷静反问保留不甘

payoff_pattern: 姐姐拒绝以妹妹死亡换来的救法，父母的预言逻辑自我崩塌，转世胎记暗示妹妹离开原家庭重获可能。

tomato_fit_score: 8.3

### 神髓禁改项

1. 死亡必须在前20%发生，灵魂只能看不能干预。
2. 父母不能写成纯坏人，必须是被预言/系统绑架的共谋者。
3. “以宁你懂点事”这类温柔残忍句必须保留功能。
4. 转世胎记必须含蓄，不要明说大团圆重生。

### 可替换项

1. 预言弹幕可替换为系统、神谕、算命、医疗概率。
2. 姐姐可替换为哥哥、病弱手足、继承人。
3. 胎记可替换为旧动作、旧物、旧称呼。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
