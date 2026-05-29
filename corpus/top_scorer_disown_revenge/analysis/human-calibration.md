# V4 人工校准清单

```yaml
slug: top_scorer_disown_revenge
genre: modern_reversal
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 成为高考状元却接到断亲书后，我举报全家被灭门.txt
- **word_count**: 11494
- **mechanisms**: [M1, M6, M3]
- **dominant_s爽点(machine)**: 死环反杀
- **tomato_fit_score(machine)**: 8.8

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看省状元从报喜到断亲再到“灭门”报案，沿着断亲书、身份陷阱和财产记录一层层翻出真相，让亲情抛弃与利益背叛同时反噬。 |
| emotional_debt_type | 见 corpus/_index.json | 亲情抛弃债 / 身份陷阱债 |
| dominant_s爽点 | 死环反杀 | 多层递进反转 |
| antagonist_violation | 见 corpus/_index.json | 家人与未婚夫把血缘、身份和利益当作抛弃主角的理由，试图用断亲书和财产转移改写她的人生位置。 |
| protagonist_stance | 见 corpus/_index.json | 冷静报案、悬疑型反杀、情绪不外放但步步推进 |
| payoff_pattern | 见 corpus/_index.json | 省状元、断亲书、灭门报案、真千金身份和利益网络多层递进反转，结尾用“利益”金句回旋未婚夫。 |
| tomato_fit_score | 8.8 | 8.8 |

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

reader_promise: 看省状元从报喜到断亲再到“灭门”报案，沿着断亲书、身份陷阱和财产记录一层层翻出真相，让亲情抛弃与利益背叛同时反噬。

emotional_debt_type: 亲情抛弃债 / 身份陷阱债

dominant_s爽点: 多层递进反转

antagonist_violation: 家人与未婚夫把血缘、身份和利益当作抛弃主角的理由，试图用断亲书和财产转移改写她的人生位置。

protagonist_stance: 冷静报案、悬疑型反杀、情绪不外放但步步推进

payoff_pattern: 省状元、断亲书、灭门报案、真千金身份和利益网络多层递进反转，结尾用“利益”金句回旋未婚夫。

tomato_fit_score: 8.8

### 神髓禁改项

1. “状元 + 断亲书 + 举报灭门”的三重 Hook 不能拆散。
2. 多层真相揭示顺序必须精密，不能一次性解释。
3. 家庭伦理痛感不能被纯悬疑吞掉。
4. 未婚夫“利益”台词必须在结尾回旋。

### 可替换项

1. 高考状元可替换为竞赛冠军、遗产继承人、项目功臣。
2. 断亲书可替换为解除收养书、放弃继承书、除名公告。
3. 灭门报案可替换为失踪、绑架、资产侵吞等强钩子。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
