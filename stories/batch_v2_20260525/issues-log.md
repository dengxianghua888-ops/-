# 五篇跑批 Issues Log

## 批次信息
- 日期: 2026-05-25
- 优化版本: v2_style_fidelity
- 执行者: Claude Opus 4.6

---

## Story #1: modern_reversal (batch_v2_01)

### 源文: hot_027a4f9448
- Genre: modern_reversal
- 源文概述: 豪门身份反转+出轨反杀+游轮揭穿
- 源文 rhythm: avg_line_chars=22.3, short_line_rate=0.318, quote_line_rate=0.376

### 第 1 次生成

**结果**: FAIL

**失败原因**:
1. 字数严重不足: 4401 chars (目标 10000-14000)
2. short_line_rate 过高: 0.500 vs source 0.318 — 过度碎片化

**诊断**:
- 风格锚定"短/碎/快"对 modern_reversal 这类源文过度执行
- 源文 avg_line_chars=22.3 说明它的"短"是相对的——不是每行10字的碎诗，而是20-25字的紧凑叙事句
- 12章各仅400字左右，需要每章扩展到800-1200字

**返工方向**:
- 每章增加更多叙事动作行（2-3子句合并为一个20-25字的行）
- 增加对白轮次（保持对白短但回合多）
- 增加旁观者反应、物件细节
- 目标: 合并碎行，将 short_line_rate 降至 0.35 以下

---

## Story #2: family_ethics (batch_v2_02)

### 源文: hot_0033ca75f8
- Genre: family_ethics
- 源文概述: 孕妻妇产科医生复仇+丈夫出轨四年+小三生子+换药+引产+离婚+事业晋升
- 源文 rhythm: avg_line_chars=19.59, short_line_rate=0.537, quote_line_rate=0.234

### 第 1 次生成

**结果**: FAIL

**失败原因**:
1. quote_line_rate 过高: 0.388 vs source 0.234 — 对话占比超标触发 quote_over_crank

**诊断**:
- style-dna.md 描述"对话占比约43%"，但 rhythm_metrics 实测 source_quote_line_rate 仅 0.234
- 差异原因: style-dna 统计的是句级含引号占比，rhythm_metrics 统计的是行级完整包含引号的比率
- 源文大量内心独白+间接引语被 style-dna 误计为"对话"
- 首次生成按43%的锚写了大量直接对话，导致 quote_over_crank

**返工方向**:
- 完全重写，以内心独白+碎句叙事为主
- 直接对话压缩为点睛式（仅关键冲突场景保留）
- quote_line_rate 目标锚定在 source ± 0.05 即 0.19-0.28

### 第 2 次生成 (重写)

**结果**: PASS

**指标**:
- nonspace chars: 10001 ✓
- rhythm_fit: pass ✓
- quote_line_rate: 0.186 (source 0.234, 合理范围内)
- AI taste words: 0 ✓

**额外修复**:
- 发现2处"此刻"(AI禁忌词)，替换为"而现在"/"但现在"

### 总结

- 返工次数: 1 (完全重写)
- 关键教训: **写作时以 rhythm_metrics 实测值为准，不信 style-dna 的描述性百分比**
- Genre 特性: family_ethics 内心独白占比极高(>60%)，对话实际很少

---

## Story #3: ancient_BE (batch_v2_03)

### 源文: hot_7910425011
- Genre: ancient_BE (虐恋火葬场)
- 源文概述: 男友+闺蜜双重背叛+保送被偷+母亲死亡+远走重生+男主疯癫追悔
- 源文 rhythm: avg_line_chars=19.63, short_line_rate=0.457, quote_line_rate=0.275

### 第 1 次生成

**结果**: FAIL

**失败原因**:
1. 字数严重不足: 5064 chars
2. short_line_rate 过高: 0.563 vs source 0.457
3. question_marks_per_k 过高: 6.83 (over-crank)

**诊断**:
- 风格锚定"短碎快"过度执行（同Story #1的问题再次出现）
- 反问句过多导致question density超标
- 首次生成总体偏诗歌化而非叙事化

### 第 2 次生成 (重写)

**结果**: rhythm PASS，字数不足 (6825)

### 第 3 次 (逐章扩展)

**结果**: PASS

**指标**:
- nonspace chars: 10002 ✓
- rhythm_fit: pass ✓
- AI taste words: 0 ✓

### 总结

- 返工次数: 2 (一次全面重写+一次多轮扩展)
- 关键教训: **首次生成字数低于7000应立即重写而非逐段补丁**
- Genre 特性: 虐恋火葬场需要充足的"暖记忆"篇幅才能让"冷现实"有落差；旧物引爆(家书)需要情绪从爱→恨的递进

---

## Story #4: ancient_sweet (batch_v2_04)

### 源文: hot_5160748d13
- Genre: ancient_sweet
- 源文概述: 古言宫斗+掌事姑姑之女复仇+低位宫女设局+层层反杀皇后+帝后双强
- 源文 rhythm: avg_line_chars=16.747, short_line_rate=0.639, quote_line_rate=0.274

### 第 1 次生成

**结果**: FAIL

**失败原因**:
1. 字数严重不足: 3780 chars (目标 10000-14000)
2. rhythm PASS，但字符密度极低

**诊断**:
- 源文 avg_line_chars=16.7 + short_line_rate=0.639 极端短碎
- 按此风格写作自然产出极低字符密度
- 12章各仅300字左右

### 第 2 次生成 (全面重写)

**结果**: FAIL (字数不足)

**指标**:
- nonspace chars: 5690
- rhythm_fit: pass

### 第 3 次 (多轮逐章扩展)

**结果**: PASS

**指标**:
- nonspace chars: 10001 ✓
- rhythm_fit: pass ✓ (avg=17.69, short=0.470, quote=0.218)
- AI taste words: 0 ✓ (修复了1处"此刻")

### 总结

- 返工次数: 3 (首次生成 + 全面重写 + 多轮扩展)
- 关键教训: **ultra-short-line源文(avg<18, short>0.6)首次生成必然严重不足，应在写作时主动增加行数而非行长**
- Genre 特性: ancient_sweet 的宫斗式短碎节奏导致自然写作字符密度极低（每行仅15-17字），需要大量补充物件细节行、环境速描行、内心碎句行才能达到字数下限

---

## Story #5: apocalypse_heroine (batch_v2_05)

### 源文: hot_2421a56ed0
- Genre: apocalypse_heroine
- 源文概述: 末世犬化症+边牧预警+逃城+丈夫控制+病毒爆发+毒地真相+舆论反转
- 源文 rhythm: avg_line_chars=17.354, short_line_rate=0.5414, quote_line_rate=0.2583

### 第 1 次生成

**结果**: FAIL

**失败原因**:
1. quote_line_rate 过高: 0.371 vs source 0.258 — 对话占比严重超标
2. question_marks_per_k 过高: 7.33 (over-crank) — 反问句过多

**诊断**:
- 该genre看起来像对话驱动（短碎行+冲突场景），但实际quote_line_rate仅0.258
- 大量内容是内心独白式的短碎叙事句，非直接对话
- 第一次生成大量对白导致quote过高，同时反问句密度超标

**返工方向**:
- 完全重写，以内心独白碎句+环境细节为主
- 直接对话压缩到关键冲突点
- 减少反问句，改用陈述式情绪句

### 第 2 次生成 (重写)

**结果**: rhythm PASS，字数不足 (8807)

### 第 3 次 (多轮逐行扩展)

**结果**: PASS

**指标**:
- nonspace chars: 10004 ✓
- rhythm_fit: pass ✓ (avg=18.829, short=0.5437, quote=0.211)
- AI taste words: 0 ✓

### 总结

- 返工次数: 2 (一次全面重写 + 一次多轮扩展)
- 关键教训: **apocalypse_heroine类genre的quote_line_rate比直觉低（0.26而非0.35+），因为大量冲突场景是通过内心独白而非对话展开的**
- Genre 特性: 内心碎句占比极高，物理环境描写用单独短行展开，扩展时每增加100字需要约8行短碎内容
- avg_line_chars ceiling敏感: source=17.35 → ceiling=21.69，扩展时必须持续监控

---

## 全批次汇总

| # | Genre | 返工次数 | 首次失败原因 | 最终nonspace |
|---|-------|---------|-------------|-------------|
| 1 | modern_reversal | 1 | 字数不足(4401) + short过高 | 10001 |
| 2 | family_ethics | 1 | quote过高(0.388 vs 0.234) | 10001 |
| 3 | ancient_BE | 2 | 字数不足 + short过高 + question过高 | 10002 |
| 4 | ancient_sweet | 3 | 字数严重不足(3780) | 10001 |
| 5 | apocalypse_heroine | 2 | quote过高(0.371) + question过高 | 10004 |

### 共性问题

1. **首次生成字数普遍不足**: 5/5篇首次生成均未达到10000下限。短碎风格导致自然写作密度低。
2. **quote_line_rate误判**: 3/5篇首次生成quote过高。style-dna描述的"对话占比"与rhythm_metrics实测值有显著差异。
3. **扩展策略**: 所有篇目均需要多轮逐行扩展。安全扩展方式是添加短碎叙事行(物件细节、环境片段、情绪单句)。

### 产线改进建议

1. **首次生成时主动超配行数**: 写作Phase应按目标字数÷(avg_line_chars×0.8)计算所需行数，确保首次生成即接近目标
2. **rhythm_metrics实测值优先**: 以source实测rhythm数据为准，不信style-dna的描述性百分比
3. **quote_line_rate锚定**: 写作时以source_quote_line_rate ± 0.05为目标区间，而非凭"对话密集"的直觉
4. **字数不足时的扩展策略标准化**: 每次添加短碎行(≤12字)，每批次后立即验证rhythm不破
