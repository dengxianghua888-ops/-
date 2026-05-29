# StoryForge Production Stability Report

## stories/prod_batch_01_autopsy_vow

### Run `20260508_211638`

- Status: unknown
- Started: 2026-05-08 21:16:38
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 97s | codex | codex | - | - | 1 artifacts ok |
| 2 | completed | 434s | codex | codex | - | - | 7 artifacts ok |
| 3 | completed | 210s | codex | codex | - | - | 2 artifacts ok |
| 4 | failed | 313s | codex | codex | - | beat-bible.json beats[1].forbidden_summary must be a non-empty list; beat-bible.json beats[2].forbidden_summary must be a non-empty list; beat-bible.json beats[3].forbidden_summary must be a non-empty list | validator failed |

### Run `20260508_213448`

- Status: unknown
- Started: 2026-05-08 21:34:48
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 422s | codex | codex | - | draft-scenes/scene-04.md length 699 outside scene card range 700-900; draft-scenes/scene-05.md length 643 outside scene card range 650-850; draft-scenes/scene-06.md length 634 outside scene card range 700-900 | validator failed |

### Run `20260508_214527`

- Status: unknown
- Started: 2026-05-08 21:45:27
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 275s | codex | codex | - | quality-report.json critic_scores.emotion must be a number from 0 to 10; quality-report.json critic_scores.logic must be a number from 0 to 10; quality-report.json critic_scores.platform must be a number from 0 to 10 | validator failed |

### Run `20260508_215429`

- Status: unknown
- Started: 2026-05-08 21:54:29
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 519s | codex | codex | - | quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 16; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0; story.yaml status must be final, submitted, or test_fixture | validator failed |

### Run `20260508_220422`

- Status: completed
- Started: 2026-05-08 22:04:22
- Ended: 2026-05-08 22:05:34

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 72s | codex | codex | - | - | 1 artifacts ok |

### Run `regen_20260514_01`

- Status: unknown
- Started: 2026-05-14 01:03:40
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | failed | 4s | codex | codex | - | - | codex returned no artifact bundle |

### Run `regen_20260514_01_escalated`

- Status: unknown
- Started: 2026-05-14 01:36:11
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 140s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 305s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string | validator failed |
| 3 | completed | 258s | codex | codex | - | - | 2 artifacts ok |
| 4 | completed | 270s | codex | codex | - | - | 16 artifacts ok |
| 5 | failed | 658s | codex | codex | - | draft-scenes/scene-14.md length 799 outside scene card range 800-1000; draft.md must equal draft-scenes joined in scene_id order | validator failed |
| 6 | failed | 258s | codex | codex | critical_failures_stringified, important_failures_stringified, machine_metrics_refreshed, review_gate_yaml_synced | review.md critical_failures does not match quality-report.json; quality gate failed: gate_status=fail | validator failed |
| 5 | failed | 1479s | codex | codex | - | draft-scenes/scene-14.md length 799 outside scene card range 800-1000; draft.md must equal draft-scenes joined in scene_id order | validator failed |

### Run `regen_20260514_01_escalated_r2`

- Status: unknown
- Started: 2026-05-14 02:05:59
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 233s | codex | codex | machine_metrics_refreshed, review_gate_yaml_synced | quality gate failed: gate_status=fail | validator failed |

### Run `regen_20260514_01_phase6_check`

- Status: unknown
- Started: 2026-05-14 02:12:04
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 236s | codex | codex | machine_metrics_refreshed, review_gate_yaml_synced | quality gate failed: gate_status=fail | validator failed |

### Run `regen_20260514_01_phase6_check2`

- Status: unknown
- Started: 2026-05-14 02:17:15
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 280s | codex | codex | important_failures_stringified, machine_metrics_refreshed, review_gate_yaml_synced | quality gate failed: gate_status=fail | validator failed |

### Run `regen_20260514_01_phase7_8`

- Status: completed
- Started: 2026-05-14 02:23:16
- Ended: 2026-05-14 02:34:04

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | completed | 580s | codex | codex | machine_metrics_refreshed | - | 21 artifacts ok |
| 8 | completed | 66s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 13180
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_02_abyss_profile

### Run `20260508_220628`

- Status: unknown
- Started: 2026-05-08 22:06:28
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 74s | codex | codex | - | - | 1 artifacts ok |
| 2 | completed | 484s | codex | codex | - | - | 7 artifacts ok |
| 3 | failed | 149s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id | validator failed |

### Run `20260508_221900`

- Status: unknown
- Started: 2026-05-08 22:19:00
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | failed | 367s | codex | codex | - | beat-bible.json beats[1].forbidden_summary must be a non-empty list; beat-bible.json beats[2].forbidden_summary must be a non-empty list; beat-bible.json beats[3].forbidden_summary must be a non-empty list | validator failed |

### Run `20260508_222550`

- Status: unknown
- Started: 2026-05-08 22:25:50
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 462s | codex | codex | - | draft-scenes/scene-02.md length 812 outside scene card range 650-780; draft-scenes/scene-09.md length 791 outside scene card range 650-780; draft-scenes/scene-13.md length 716 outside scene card range 720-880 | validator failed |

### Run `20260508_223532`

- Status: unknown
- Started: 2026-05-08 22:35:32
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 205s | codex | codex | - | quality-report.json critic_scores.emotion must be a number from 0 to 10; quality-report.json critic_scores.logic must be a number from 0 to 10; quality-report.json critic_scores.platform must be a number from 0 to 10 | validator failed |

### Run `20260508_224135`

- Status: unknown
- Started: 2026-05-08 22:41:35
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 526s | codex | codex | - | chapter_hooks: coverage 0.9375 below 1.0; quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 16; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 0.9375 | validator failed |

### Run `20260508_225124`

- Status: completed
- Started: 2026-05-08 22:51:24
- Ended: 2026-05-08 22:52:49

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 85s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 12850
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_03_empress_exit

### Run `20260508_225315`

- Status: unknown
- Started: 2026-05-08 22:53:15
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 106s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 536s | codex | codex | - | story-brief.json payoff_pattern must be a non-empty string | validator failed |

### Run `20260508_230453`

- Status: unknown
- Started: 2026-05-08 23:04:53
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 205s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id | validator failed |

### Run `20260508_230842`

- Status: unknown
- Started: 2026-05-08 23:08:42
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | failed | 327s | codex | codex | - | beat-bible.json beats[1].forbidden_summary must be a non-empty list; beat-bible.json beats[2].forbidden_summary must be a non-empty list; beat-bible.json beats[3].forbidden_summary must be a non-empty list | validator failed |

### Run `20260508_231447`

- Status: unknown
- Started: 2026-05-08 23:14:47
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 458s | codex | codex | - | draft-scenes/scene-02.md length 908 outside scene card range 1000-1250; draft-scenes/scene-03.md length 804 outside scene card range 1000-1250; draft-scenes/scene-04.md length 846 outside scene card range 1100-1350 | validator failed |

### Run `20260508_232658`

- Status: unknown
- Started: 2026-05-08 23:26:58
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 283s | codex | codex | - | quality-report.json critic_scores.emotion must be a number from 0 to 10; quality-report.json critic_scores.logic must be a number from 0 to 10; quality-report.json critic_scores.platform must be a number from 0 to 10 | validator failed |

### Run `20260508_233328`

- Status: unknown
- Started: 2026-05-08 23:33:28
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 619s | codex | codex | - | quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 15; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0; story.yaml status must be final, submitted, or test_fixture | validator failed |

### Run `20260508_234436`

- Status: completed
- Started: 2026-05-08 23:44:36
- Ended: 2026-05-08 23:46:16

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 99s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 14463
- Chapter count: 15
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_04_blossom_network

### Run `20260508_234652`

- Status: unknown
- Started: 2026-05-08 23:46:52
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 79s | codex | codex | - | - | 1 artifacts ok |
| 2 | completed | 453s | codex | codex | - | - | 7 artifacts ok |
| 3 | completed | 182s | codex | codex | - | - | 2 artifacts ok |
| 4 | failed | 276s | codex | codex | - | beat-bible.json beats[1].forbidden_summary must be a non-empty list; beat-bible.json beats[2].forbidden_summary must be a non-empty list; beat-bible.json beats[3].forbidden_summary must be a non-empty list | validator failed |

### Run `20260509_000404`

- Status: unknown
- Started: 2026-05-09 00:04:04
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 380s | codex | codex | - | draft-scenes/scene-02.md length 596 outside scene card range 650-900; draft-scenes/scene-04.md length 652 outside scene card range 700-950; draft-scenes/scene-05.md length 612 outside scene card range 650-900 | validator failed |

### Run `20260509_001334`

- Status: unknown
- Started: 2026-05-09 00:13:34
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 193s | codex | codex | - | quality-report.json machine_metrics.soft_forbidden_words.status must be pass or fail; quality-report.json critic_scores.emotion must be a number from 0 to 10; quality-report.json critic_scores.logic must be a number from 0 to 10 | validator failed |

### Run `20260509_001841`

- Status: unknown
- Started: 2026-05-09 00:18:41
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 455s | codex | codex | - | quality-report.json machine_metrics.target_length.actual does not match machine recompute: 11341 != 11427; quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 16; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0 | validator failed |

### Run `20260509_002706`

- Status: unknown
- Started: 2026-05-09 00:27:06
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|

### Run `20260509_002948`

- Status: completed
- Started: 2026-05-09 00:29:48
- Ended: 2026-05-09 00:31:17

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 88s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 11537
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_05_allowance_truth

### Run `20260509_003137`

- Status: unknown
- Started: 2026-05-09 00:31:37
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 119s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 264s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string; story-brief.json payoff_pattern must be a non-empty string | validator failed |

### Run `20260509_003837`

- Status: unknown
- Started: 2026-05-09 00:38:37
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | completed | 162s | codex | codex | - | - | 2 artifacts ok |
| 4 | failed | 268s | codex | codex | - | beat-bible.json beats[1].forbidden_summary must be a non-empty list; beat-bible.json beats[2].forbidden_summary must be a non-empty list; beat-bible.json beats[3].forbidden_summary must be a non-empty list | validator failed |

### Run `20260509_004622`

- Status: unknown
- Started: 2026-05-09 00:46:22
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 435s | codex | codex | - | draft-scenes/scene-02.md length 898 outside scene card range 750-850; draft-scenes/scene-06.md length 716 outside scene card range 750-850; draft-scenes/scene-07.md length 676 outside scene card range 700-800 | validator failed |

### Run `20260509_005648`

- Status: unknown
- Started: 2026-05-09 00:56:48
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 266s | codex | codex | - | quality-report.json critic_scores.emotion must be a number from 0 to 10; quality-report.json critic_scores.logic must be a number from 0 to 10; quality-report.json critic_scores.platform must be a number from 0 to 10 | validator failed |

### Run `20260509_010412`

- Status: unknown
- Started: 2026-05-09 01:04:12
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 507s | codex | codex | - | chapter_length: ch02 has 1337 chars, expected 500-1200; chapter_length: ch03 has 1557 chars, expected 500-1200; chapter_length: ch04 has 1465 chars, expected 500-1200 | validator failed |

### Run `20260509_011405`

- Status: completed
- Started: 2026-05-09 01:14:05
- Ended: 2026-05-09 01:15:17

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 72s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 13165
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_06_moon_spring

### Run `20260511_102406`

- Status: unknown
- Started: 2026-05-11 10:24:06
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|

### Run `20260511_102709`

- Status: unknown
- Started: 2026-05-11 10:27:09
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 112s | codex | codex | - | - | 1 artifacts ok |
| 2 | completed | 570s | codex | codex | - | - | 7 artifacts ok |
| 3 | completed | 152s | codex | codex | - | - | 2 artifacts ok |
| 4 | completed | 492s | codex | codex | - | - | 21 artifacts ok |
| 5 | failed | 499s | codex | codex | - | draft-scenes/scene-01.md length 618 outside scene card range 750-850; draft-scenes/scene-02.md length 630 outside scene card range 700-800; draft-scenes/scene-03.md length 582 outside scene card range 700-800 | validator failed |

### Run `20260511_105848`

- Status: unknown
- Started: 2026-05-11 10:58:48
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 476s | codex | codex | - | draft-scenes/scene-01.md length 491 outside scene card range 750-850; draft-scenes/scene-02.md length 530 outside scene card range 700-800; draft-scenes/scene-03.md length 514 outside scene card range 700-800 | validator failed |

### Run `20260511_110756`

- Status: unknown
- Started: 2026-05-11 11:07:56
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 202s | codex | codex | - | quality-report.json critic_scores.emotion must be a number from 0 to 10; quality-report.json critic_scores.logic must be a number from 0 to 10; quality-report.json critic_scores.platform must be a number from 0 to 10 | validator failed |

### Run `20260511_111427`

- Status: unknown
- Started: 2026-05-11 11:14:27
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 866s | codex | codex | - | quality-report.json machine_metrics.target_length.actual does not match machine recompute: 10119 != 10039; quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 10; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0 | validator failed |

### Run `20260511_112930`

- Status: completed
- Started: 2026-05-11 11:29:30
- Ended: 2026-05-11 11:31:07

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 96s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10217
- Chapter count: 10
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_07_fake_princess_friends

### Run `20260511_113236`

- Status: unknown
- Started: 2026-05-11 11:32:36
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 104s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 331s | codex | codex | - | story-brief.json payoff_pattern must be a non-empty string | validator failed |

### Run `20260511_114052`

- Status: unknown
- Started: 2026-05-11 11:40:52
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 254s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id; adaptation-room.json mechanism_preservation must be a non-empty object | validator failed |

### Run `20260511_114552`

- Status: unknown
- Started: 2026-05-11 11:45:52
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | failed | 330s | codex | codex | - | beat-bible.json beats[1].forbidden_summary must be a non-empty list; beat-bible.json beats[2].forbidden_summary must be a non-empty list; beat-bible.json beats[3].forbidden_summary must be a non-empty list | validator failed |

### Run `20260511_115200`

- Status: unknown
- Started: 2026-05-11 11:52:00
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 351s | codex | codex | - | draft-scenes/scene-01.md length 608 outside scene card range 820-980; draft-scenes/scene-02.md length 613 outside scene card range 820-980; draft-scenes/scene-03.md length 559 outside scene card range 860-1050 | validator failed |

### Run `20260511_120838`

- Status: unknown
- Started: 2026-05-11 12:08:38
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 322s | codex | codex | - | quality gate failed: gate_status=fail | validator failed |

### Run `20260511_121937`

- Status: unknown
- Started: 2026-05-11 12:19:37
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 493s | codex | codex | - | quality-report.json machine_metrics.target_length.actual does not match machine recompute: 10369 != 10387; quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 14; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0 | validator failed |

### Run `20260511_122838`

- Status: completed
- Started: 2026-05-11 12:28:38
- Ended: 2026-05-11 12:30:30

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 111s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10652
- Chapter count: 14
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_08_hotel_group

### Run `20260511_123050`

- Status: unknown
- Started: 2026-05-11 12:30:50
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 116s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 363s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string; story-brief.json payoff_pattern must be a non-empty string | validator failed |

### Run `20260511_123920`

- Status: unknown
- Started: 2026-05-11 12:39:20
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 173s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id | validator failed |

### Run `20260511_124247`

- Status: unknown
- Started: 2026-05-11 12:42:47
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | failed | 329s | codex | codex | - | beat-bible.json beats[1] missing required keys: chapter_end_hook; beat-bible.json beats[3] missing required keys: chapter_end_hook; beat-bible.json beats[5] missing required keys: chapter_end_hook | validator failed |

### Run `20260511_124847`

- Status: unknown
- Started: 2026-05-11 12:48:47
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 370s | codex | codex | - | draft-scenes/scene-08.md length 530 outside scene card range 550-700; draft-scenes/scene-09.md length 590 outside scene card range 600-750; draft-scenes/scene-10.md length 572 outside scene card range 600-750 | validator failed |

### Run `20260511_125618`

- Status: unknown
- Started: 2026-05-11 12:56:18
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 226s | codex | codex | - | quality gate failed: gate_status=fail | validator failed |

### Run `20260511_130620`

- Status: unknown
- Started: 2026-05-11 13:06:20
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 458s | codex | codex | - | quality-report.json machine_metrics.target_length.actual does not match machine recompute: 10303 != 10415; quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 16; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0 | validator failed |

### Run `20260511_131443`

- Status: completed
- Started: 2026-05-11 13:14:43
- Ended: 2026-05-11 13:16:31

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 107s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10529
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_09_streamer_exit

### Run `20260511_131648`

- Status: unknown
- Started: 2026-05-11 13:16:48
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 150s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 342s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string | validator failed |

### Run `20260511_132552`

- Status: unknown
- Started: 2026-05-11 13:25:52
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 298s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id; adaptation-room.json mechanism_preservation must be a non-empty object | validator failed |

### Run `20260511_133120`

- Status: unknown
- Started: 2026-05-11 13:31:20
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | completed | 306s | codex | codex | - | - | 16 artifacts ok |
| 5 | failed | 513s | codex | codex | - | draft-scenes/scene-01.md length 746 outside scene card range 900-1000; draft-scenes/scene-02.md length 729 outside scene card range 950-1050; draft-scenes/scene-03.md length 827 outside scene card range 1000-1100 | validator failed |

### Run `20260511_134600`

- Status: unknown
- Started: 2026-05-11 13:46:00
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 182s | codex | codex | - | review.md critical_failures does not match quality-report.json; quality gate failed: gate_status=fail | validator failed |

### Run `20260511_135305`

- Status: unknown
- Started: 2026-05-11 13:53:05
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 7 | failed | 475s | codex | codex | - | quality-report.json machine_metrics.target_length.actual does not match machine recompute: 10892 != 11366; quality-report.json machine_metrics.chapters.count does not match machine recompute: 0 != 15; quality-report.json machine_metrics.chapters.hook_coverage does not match machine recompute: 0.0 != 1.0 | validator failed |

### Run `20260511_140128`

- Status: completed
- Started: 2026-05-11 14:01:28
- Ended: 2026-05-11 14:02:49

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 81s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 11559
- Chapter count: 15
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_10_tang_flower

### Run `20260511_140334`

- Status: unknown
- Started: 2026-05-11 14:03:34
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|

### Run `20260511_140426`

- Status: unknown
- Started: 2026-05-11 14:04:26
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 89s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 242s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string | validator failed |

### Run `20260511_141035`

- Status: unknown
- Started: 2026-05-11 14:10:35
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 251s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id | validator failed |

### Run `20260511_141514`

- Status: unknown
- Started: 2026-05-11 14:15:14
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | completed | 457s | codex | codex | - | - | 17 artifacts ok |
| 5 | failed | 365s | codex | codex | - | draft-scenes/scene-01.md length 606 outside scene card range 750-850; draft-scenes/scene-02.md length 614 outside scene card range 750-850; draft-scenes/scene-03.md length 609 outside scene card range 750-850 | validator failed |

### Run `20260511_143401`

- Status: unknown
- Started: 2026-05-11 14:34:01
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 180s | codex | codex | - | quality gate failed: gate_status=fail | validator failed |

### Run `20260511_144415`

- Status: unknown
- Started: 2026-05-11 14:44:15
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|

### Run `20260511_145800`

- Status: completed
- Started: 2026-05-11 14:58:00
- Ended: 2026-05-11 14:59:35

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 95s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10717
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_11_drowning_divorce

### Run `20260511_145955`

- Status: unknown
- Started: 2026-05-11 14:59:55
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 154s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 461s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string; story-brief.json payoff_pattern must be a non-empty string | validator failed |

### Run `20260511_151044`

- Status: unknown
- Started: 2026-05-11 15:10:44
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 237s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id | validator failed |

### Run `20260511_151533`

- Status: unknown
- Started: 2026-05-11 15:15:33
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | completed | 322s | codex | codex | - | - | 17 artifacts ok |
| 5 | failed | 503s | codex | codex | - | draft-scenes/scene-01.md length 665 outside scene card range 900-1100; draft-scenes/scene-02.md length 822 outside scene card range 900-1100; draft-scenes/scene-03.md length 805 outside scene card range 900-1100 | validator failed |

### Run `20260511_153116`

- Status: unknown
- Started: 2026-05-11 15:31:16
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | completed | 211s | codex | codex | - | - | 7 artifacts ok |
| 7 | failed | 503s | codex | codex | - | quality-report.json machine_metrics.target_length.actual does not match machine recompute: 11391 != 12014; quality-report.json machine_metrics.paywall_cards.required does not match machine recompute: 5 != 4; quality-report.json machine_metrics.paywall_cards.actual does not match machine recompute: 5 != 10 | validator failed |

### Run `20260511_154352`

- Status: completed
- Started: 2026-05-11 15:43:52
- Ended: 2026-05-11 15:45:48

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 116s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 12211
- Chapter count: 16
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_12_top_scorer_report

### Run `20260511_154627`

- Status: unknown
- Started: 2026-05-11 15:46:27
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 130s | codex | codex | - | - | 1 artifacts ok |
| 2 | failed | 287s | codex | codex | - | story-brief.json hook_type must be a non-empty string; story-brief.json title_formula must be a non-empty string; story-brief.json payoff_pattern must be a non-empty string | validator failed |

### Run `20260511_155443`

- Status: unknown
- Started: 2026-05-11 15:54:43
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | completed | 211s | codex | codex | - | - | 2 artifacts ok |
| 4 | completed | 295s | codex | codex | - | - | 16 artifacts ok |

### Run `20260511_161316`

- Status: unknown
- Started: 2026-05-11 16:13:16
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 5 | failed | 394s | codex | codex | - | draft-scenes/scene-01.md length 641 outside scene card range 780-920; draft-scenes/scene-02.md length 658 outside scene card range 760-900; draft-scenes/scene-03.md length 664 outside scene card range 760-920 | validator failed |

### Run `20260511_162146`

- Status: unknown
- Started: 2026-05-11 16:21:46
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | failed | 175s | codex | codex | - | quality gate failed: gate_status=fail | validator failed |

### Run `20260511_163146`

- Status: unknown
- Started: 2026-05-11 16:31:46
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|

### Run `20260511_163841`

- Status: completed
- Started: 2026-05-11 16:38:41
- Ended: 2026-05-11 16:40:21

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 100s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10500
- Chapter count: 15
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_13_customs_package

### Run `20260511_164056`

- Status: unknown
- Started: 2026-05-11 16:40:56
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 136s | codex | codex | - | - | 1 artifacts ok |

### Run `20260511_165015`

- Status: unknown
- Started: 2026-05-11 16:50:15
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 3 | failed | 202s | codex | codex | - | adaptation-room.json selected_candidate must match a candidate id | validator failed |

### Run `20260511_165411`

- Status: unknown
- Started: 2026-05-11 16:54:11
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 4 | completed | 302s | codex | codex | - | - | 16 artifacts ok |

### Run `20260511_171733`

- Status: unknown
- Started: 2026-05-11 17:17:33
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 6 | completed | 182s | codex | codex | - | - | 7 artifacts ok |

### Run `20260511_172849`

- Status: completed
- Started: 2026-05-11 17:28:49
- Ended: 2026-05-11 17:30:40

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 8 | completed | 111s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10300
- Chapter count: 15
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_14_spring_ming

### Run `20260511_173147`

- Status: unknown
- Started: 2026-05-11 17:31:47
- Ended: -

| Phase | Status | Duration | Runner | Provider | Normalizer | Failures | Notes |
|---:|---|---:|---|---|---|---|---|
| 1 | completed | 111s | codex | codex | - | - | 1 artifacts ok |

Final Phase 8 Metrics:

- Target length actual: 10326
- Chapter count: 15
- Chapter hook coverage: 1.0
- Failures: -

## stories/prod_batch_15_drug_mom_revenge

No runs found.
