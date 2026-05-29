# context/ 跨案例经验沉淀(V3)

> 本目录替代旧的单文件 `context.md`(保留作人类笔记入口),结构化存储跨案例的机制执行经验、违禁词学习、Style DNA 统计等。

## 文件

- `forbidden-words-learned.json` — 按 genre 新发现的违禁/AI 惯性词。单词在 ≥3 案例出现 → 升级到正式违禁列表
- `mechanism-playbook.json` — M1-M8 各机制的 success_cases + failure_patterns
- `style-dna-stats.json` — 各 genre 的 Style DNA 定量字段均值/方差/样本

## 写入时机

- **finalizer Step 5**:每次跑批完成后,按 genre 写入新违禁词 + 机制成败经验
- **dissector**(读):Step 3 Style DNA 时参考 `style-dna-stats.json` 的 genre 均值作为先验
- **adapter**(读):生成方案前参考 `mechanism-playbook.json` 的 success_cases 作 few-shot

## 升级机制

当某个词在 `forbidden-words-learned.json` 下某个 genre 出现 ≥3 次:
1. 把它加入 `prompts/patterns/forbidden-and-preferred.md` 对应 genre 段落
2. 从 `forbidden-words-learned.json` 移除,或标记为 `promoted: true`
3. 更新 `_meta.updated_at`
