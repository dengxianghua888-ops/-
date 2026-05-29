# V4 人工校准计划

- **generated_at**: 2026-04-26 23:29:34
- **target_per_genre**: 2
- **status**: pending_human_review

## 校准候选

| genre | slug | score | mechanisms | checklist |
|-------|------|-------|------------|-----------|
| ancient_BE | dead_autopsy_pregnant | 8.2 | M4, M5, M1 | corpus/dead_autopsy_pregnant/analysis/human-calibration.md |
| ancient_BE | ancient_mother_emperor_regret | 8.0 | M5, M4, M8, M6 | corpus/ancient_mother_emperor_regret/analysis/human-calibration.md |
| ancient_sweet | ancient_sweet_blossom | 8.2 | M2, M3, M6 | corpus/ancient_sweet_blossom/analysis/human-calibration.md |
| apocalypse_heroine | apocalypse_exile_revenge | 8.2 | M7, M6, M8 | corpus/apocalypse_exile_revenge/analysis/human-calibration.md |
| apocalypse_heroine | abyss_codename | 8.0 | M2, M6, M7 | corpus/abyss_codename/analysis/human-calibration.md |
| family_ethics | husband_drug_mom_revenge | 8.7 | M3, M1, M5 | corpus/husband_drug_mom_revenge/analysis/human-calibration.md |
| family_ethics | sister_rebirth_my_death | 8.1 | M4, M5, M3 | corpus/sister_rebirth_my_death/analysis/human-calibration.md |
| modern_reversal | top_scorer_disown_revenge | 8.8 | M1, M6, M3 | corpus/top_scorer_disown_revenge/analysis/human-calibration.md |
| modern_reversal | hermes_customs_package | 8.7 | M1, M3 | corpus/hermes_customs_package/analysis/human-calibration.md |
| urban_sweet_ceo | airdrop_company_ceo | 8.1 | M2, M3, M5 | corpus/airdrop_company_ceo/analysis/human-calibration.md |

## 使用方式

1. 人工阅读对应 `dissection.md` 与 V4 四件套。
2. 填写每个 `human-calibration.md` 的人工校准列、禁改项、可替换项和备注。
3. 只有当 `decision: approved` 且 reviewer/reviewed_at 已填写时,才允许升级为 `human_calibrated`。

注意: 本计划只创建校准工作台,不会自动把 machine_draft 标记为 human_calibrated。
