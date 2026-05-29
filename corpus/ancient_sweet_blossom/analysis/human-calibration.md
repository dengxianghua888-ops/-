# V4 人工校准清单

```yaml
slug: ancient_sweet_blossom
genre: ancient_sweet
v4_calibration_status: approved_codex_review
previous_status: machine_draft
reviewer: "Codex-AI review requested by user"
reviewed_at: "2026-04-27"
decision: approved # pending|approved|revise
```

## 案例信息

- **filename**: 《盼我流年，花满蹊径》.txt
- **word_count**: 14953
- **mechanisms**: [M2, M3, M6]
- **dominant_s爽点(machine)**: 身份反差爆发
- **tomato_fit_score(machine)**: 8.2

## 机器基因草稿与校准结论

| 字段 | machine_draft | 人工校准 |
|------|---------------|----------|
| reader_promise | 见 corpus/_index.json | 看被假千金嘲成一事无成的嫡女，靠藏住的人脉、身份和能力一层层轻快打脸，并获得双强甜宠补偿。 |
| emotional_debt_type | 见 corpus/_index.json | 轻辱反差债 / 身份低估债 |
| dominant_s爽点 | 身份反差爆发 | 身份反差爆发 |
| antagonist_violation | 见 corpus/_index.json | 假千金和势利者用身份偏见贬低女主，把“无能”标签强贴到真正有资源的人身上。 |
| protagonist_stance | 见 corpus/_index.json | 松弛、聪明、藏锋、俏皮不苦大仇深 |
| payoff_pattern | 见 corpus/_index.json | 女主的朋友、人脉和身份逐层揭开，羞辱者意识到自己一直在输，男主识破并站到同一阵营。 |
| tomato_fit_score | 8.2 | 8.3 |

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

reader_promise: 看被假千金嘲成一事无成的嫡女，靠藏住的人脉、身份和能力一层层轻快打脸，并获得双强甜宠补偿。

emotional_debt_type: 轻辱反差债 / 身份低估债

dominant_s爽点: 身份反差爆发

antagonist_violation: 假千金和势利者用身份偏见贬低女主，把“无能”标签强贴到真正有资源的人身上。

protagonist_stance: 松弛、聪明、藏锋、俏皮不苦大仇深

payoff_pattern: 女主的朋友、人脉和身份逐层揭开，羞辱者意识到自己一直在输，男主识破并站到同一阵营。

tomato_fit_score: 8.3

### 神髓禁改项

1. “一事无成”与“朋友多/资源多”的反差核心不可换。
2. 身份/人脉至少三层递进揭开，不能一次性摊牌。
3. 男主必须识破并并肩，而不是单纯救场。
4. 甜宠语气要压住复仇戾气，保持轻快打脸。

### 可替换项

1. 相府/江湖可替换为书院、商会、宗门、宫廷。
2. 假千金可替换为庶妹、表姐、冒名者。
3. 江湖人脉可替换为师门、人情债、商路、旧部。

### 校准备注

本轮由 Codex 根据用户请求完成代审判断。状态可由 `apply-human-calibration.py` 升级,但 reviewer 字段保留 AI 代审来源,便于后续真人复核。
