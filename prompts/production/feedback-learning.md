# Feedback Learning Contract

输出 `feedback-learning.json`,用于下一篇检索和复盘。

必须包含:
- `story_slug`, `pipeline_mode`, `genre`, `mechanisms`, `target_length`, `final_length`
- `quality_scores`: 必须包含 `platform`、`emotion`、`style`、`logic`,并与 `quality-report.json.critic_scores` 一致
- `failure_types`: 失败类型列表;没有失败也必须输出空数组
- `successful_hooks`
- `paywall_cards`
- `new_forbidden_candidates`
- `retrieval_tags`
- `manual_revision_delta`: 若无人类修订则为空数组

要求:
- 只沉淀可复用事实,不要写空泛心得。
- 失败项必须能回指到 scene_id 或 chapter。
