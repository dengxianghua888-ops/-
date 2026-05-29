# Style DNA

## 体感判定
- 风格标签：`高密度短句`、`对白推进`、`连续误判`、`倒计时驱动`、`每小段必抬压`
- 叙事姿态：第一人称近景，信息刻意克制，主角知道更多但绝不一次说透。
- 快节奏锁定：`是`
- 锁定说明：
  - 仿写不得用解释性长段替代现场冲突。
  - 仿写不得用流程清单替代“我现在就得跑”的即时动作。
  - 仿写不得用情绪总结替代老师、警察、家长、朋友的现场压迫。

## 机器可读指标
```yaml
avg_sentence_len_chars: 15.8
avg_visual_line_len_chars: 13.6
short_line_rate_le_16: 0.74
long_line_rate_ge_40: 0.05
direct_dialogue_line_rate: 0.56
bullet_comment_line_rate: 0.00
dialogue_ratio: 0.61
question_mark_density_per_1000_chars: 5.8
exclamation_mark_density_per_1000_chars: 7.6
golden_line_density_per_1000_chars: 2.1
```

## 指标解释
- `平均句长低`
  - 绝大多数句子承担单一功能：动作、判断、施压、打断、升级。
- `平均可视行长更低`
  - 原文利用大量断行制造“急促呼吸感”。
- `对白行率高`
  - 群像压力不是旁白说出来的，而是靠老师、考生、闺蜜、警察、家长轮流开口压迫。
- `问号密度中高`
  - 主要来自质问、猜测和否认，持续制造认知不稳定。
- `感叹号密度高`
  - 用于倒计时、喊话、群体骂声、求救场面，增强现场爆裂感。
- `金句密度不靠文艺`
  - 金句更像规则句或任务句，例如“那是催命的倒计时”“里面只有时间，乱掉的时间”。

## 语言手法
- 高频句型：
  - “不，X不是……”
  - “再不X就来不及了”
  - “我不能说”
  - “他们都不相信我”
  - “没人发现……”
- 推进方式：
  - 每提出一个猜测，立刻打掉它。
  - 每获得一点缓冲，立刻追加更大危险。
  - 每当主角想解释，环境就升级到不容解释的地步。
- 句法偏好：
  - 短陈述句。
  - 短对白对撞。
  - 小段落独立成屏。
  - 很少出现长修辞、长比喻、抒情回旋。

## 场面调度 DNA
- 常用镜头：
  - 挂钟、手表、铃声、雨、门、墙、楼层、地下室。
- 常用压迫源：
  - 公共秩序代表：监考、巡考、警察。
  - 道德审判代表：家长、闺蜜母亲、群体考生。
  - 情感背刺代表：闺蜜、父母。
- 常用升级方式：
  - 从口头不信 -> 身体控制 -> 资格剥夺 -> 人际决裂 -> 群体围攻 -> 官方介入 -> 规则实锤。

## 节奏契约 `rhythm_contract`
```yaml
avg_visual_line_len_range: [11.5, 15.5]
short_line_rate_range: [0.68, 0.82]
direct_dialogue_line_rate_range: [0.48, 0.62]
bullet_comment_line_rate_range: [0.00, 0.03]
question_mark_density_range_per_1000_chars: [4.5, 7.5]
exclamation_mark_density_range_per_1000_chars: [6.0, 9.0]
min_hooks_per_chapter: 1
min_rhetorical_questions_per_chapter: 1
min_evidence_reversals_per_chapter: 1
```

## 必守文风红线
- 不能把主角写成冷静分析员；她必须是强压下的急迫行动者。
- 不能把真相一次性解释完；必须让“半真相”先驱动冲突。
- 不能减少对白密度；群体误判感来自多人出声。
- 不能把灾变写成背景介绍；必须让读者跟着倒计时一格格逼近。
- 不能把结尾系统线铺得太早；本篇主体仍是考场救人，不是系统说明会。
