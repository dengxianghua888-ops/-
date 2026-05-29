# 五篇新产出稳定性与像素级节奏复盘

## 总览

| 序号 | 标题 | 字数 | 章节 | Rubric | 钩子 | 源/稿均行 | 源/稿短行率 | 源/稿对白率 | 源/稿问号/k | 生产痕迹 |
|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | 他逼我小产后，才知我是公主 | 10124 | 14 | 9.8 | 14/14 强钩,弱钩章: 无 | 24.937/22.253 | 0.263/0.385 | 0.416/0.535 | 4.538/6.836 | 0 |
| 2 | 高考出分后，姥爷逼我找回不存在的弟弟 | 10005 | 14 | 9.82 | 13/14 强钩,弱钩章: ch10 | 19.869/18.795 | 0.401/0.475 | 0.278/0.429 | 5.811/7.237 | 0 |
| 3 | 一手捧红的短剧顶流嫌我老，我连夜改捧他的死对头 | 10007 | 14 | 9.63 | 13/14 强钩,弱钩章: ch05 | 23.95/19.821 | 0.383/0.375 | 0.431/0.401 | 7.058/3.153 | 0 |
| 4 | 棠花落尽不相逢 | 10538 | 14 | 9.78 | 13/14 强钩,弱钩章: ch10 | 20.09/17.665 | 0.411/0.466 | 0.347/0.408 | 4.055/1.54 | 0 |
| 5 | 被养兄弃在黑港三年后，我跳塔了 | 10319 | 15 | 9.8 | 14/15 强钩,弱钩章: ch01 | 20.43/18.179 | 0.424/0.461 | 0.246/0.288 | 4.623/2.07 | 0 |

## 结论

- 五篇最终均通过 Phase 7 validator、source_rhythm_fit 与番茄 rubric；Rubric 分数区间 9.63-9.82。
- 生产痕迹命中 0，移动端段落违规 0；最终正文、分章正文均未检出代码围栏、本地路径、评语腔或异常标点。
- 本轮重点从“生成端重跑”推进到“封装层审稿”：清掉卡片尾句、尾部复述和非叙事提问后，五篇仍稳定过线。

## 产线优化

- 封装器保留源文段落节拍，只在缺句末标点时补最小标点，避免把原文快节奏拆成机械短句。
- 新增半句合并：段落以逗号、顿号、冒号、分号收尾时先并入下一段，禁止生成“，。”类伪标点。
- 新增生产痕迹硬扫：代码围栏、本地路径、截断句、事实层面、主线爽感、社会性新生等评语腔进入 fail gate。
- 新增无引号悬念提问过滤：场景卡式“为什么/是什么/有没有”尾句不允许进入正文。
- 新增章尾近邻去重：章尾钩子如果复述近 14 段内已出现的台词或句子，自动删除重复尾巴。
- 场景卡字段值作为污染候选，独立段落若等同于卡片信息缺口或效果说明，封装时丢弃。
- 临界低字数只补具体动作细节，不再为了凑字数补解释性总结。

## 仍需盯防

- 现代题材的问号密度仍可能低于源文，应在下一轮把“质问/反问密度”从观察项提升为题材自适应门槛。
- 长源文样本应继续默认 batch-size=1 或失败后自动降级，减少漏交和协议漂移。
- 补字优先补动作、物件、场面反应；严禁补主题解释、人物总结和卡片式信息缺口。

## 返工点摘录

### 他逼我小产后，才知我是公主
- split attempts: 11, failed attempts: 6
- draft-scenes/scene-01.md chars 666 below min 680; draft-scenes/scene-01.md avg_line_chars 8.22 below 11.0; merge mechanical fragments
- draft-scenes/scene-01.md chars 963 above max 760; draft-scenes/scene-01.md avg_line_chars 19.65 above 18; tighten lines
- draft-scenes/scene-01.md chars 662 below min 680; draft-scenes/scene-01.md avg_line_chars 8.07 below 11.0; merge mechanical fragments
- draft-scenes/scene-13.md chars 666 below min 720; draft-scenes/scene-14.md chars 472 below min 560
- artifact_parse: missing expected scene outputs: draft-scenes/scene-14.md
- artifact_parse: missing expected scene outputs: draft-scenes/scene-14.md

### 高考出分后，姥爷逼我找回不存在的弟弟
- split attempts: 7, failed attempts: 0
- 无正文批次失败。

### 一手捧红的短剧顶流嫌我老，我连夜改捧他的死对头
- split attempts: 9, failed attempts: 2
- draft-scenes/scene-01.md chars 660 below min 700
- draft-scenes/scene-13.md chars 674 below min 760; draft-scenes/scene-14.md chars 642 below min 680

### 棠花落尽不相逢
- split attempts: 22, failed attempts: 10
- draft-scenes/scene-01.md chars 681 below min 720
- draft-scenes/scene-05.md chars 644 below min 700
- artifact_parse: missing expected scene outputs: draft-scenes/scene-06.md
- artifact_parse: missing expected scene outputs: draft-scenes/scene-06.md
- artifact_parse: missing expected scene outputs: draft-scenes/scene-06.md
- draft-scenes/scene-07.md chars 707 below min 720

### 被养兄弃在黑港三年后，我跳塔了
- split attempts: 24, failed attempts: 9
- draft-scenes/scene-03.md chars 621 below min 660
- artifact_parse: no artifact blocks found
- artifact_parse: no artifact blocks found
- artifact_parse: no artifact blocks found
- draft-scenes/scene-09.md chars 611 below min 680
- draft-scenes/scene-12.md chars 713 below min 740
