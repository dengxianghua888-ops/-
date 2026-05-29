# V4 Smoke Test Run Report

## Test Setup

- story: `stories/v4_smoke_local_rules`
- mode: local manual smoke test
- reason: real auto run on `stories/v4_smoke_gaokao_inheritance` failed at external Claude API connection and escalation was rejected due local-only third-party source risk.
- successful run id: `v4_smoke_manual_20260427_02`
- failed auto run id: `stories/v4_smoke_gaokao_inheritance/runs/v4_smoke_20260427_01`

## Expected Coverage

- pipeline manual phase sequencing
- required V4 artifacts
- structured review gate
- nested `quality-report.json` validator
- final `story.yaml` validation
- workspace-policy forbidden-word validation

## Attempt 0: Real Auto Run On Local Corpus Source

- command: `./pipeline.sh --story stories/v4_smoke_gaokao_inheritance --auto --run-id v4_smoke_20260427_01 --max-retries 1`
- input: copied from `corpus/gaokao_inheritance_brother/source.md`
- result: failed in Phase 1 after 183s
- phase summary: `Phase 1 | failed | prompts/dissector.md | model=sonnet | auto-phase exit nonzero`
- auto log tail: `API Error: Unable to connect to API (ConnectionRefused)`

### Problem

Auto mode depends on external Claude API access. The sandboxed run cannot connect. Escalated rerun was rejected because it would send local third-party source text to an external API. This is a deployment/runtime problem, not a V4 artifact validator problem.

### Impact

- `--auto` cannot currently be used for local-only copyrighted corpus sources in this environment.
- The pipeline did correctly capture stdout/stderr into `phase1.auto.log` and wrote a failed phase summary.

## Attempt 1: Manual Mode Without TTY

- command: `./pipeline.sh --story stories/v4_smoke_local_rules --run-id v4_smoke_manual_20260427_01 --max-retries 1`
- result: failed immediately at Phase 1 prompt because `read -r` had no interactive stdin.

### Problem

Manual mode requires a real TTY. Running it as a plain non-interactive command exits at the first human checkpoint.

### Impact

Manual mode is fine for terminal use, but automation wrappers must allocate a TTY or use `--auto`.

## Attempt 2: Manual Mode With TTY

- command: `./pipeline.sh --story stories/v4_smoke_local_rules --run-id v4_smoke_manual_20260427_02 --max-retries 1`
- result: completed

| Phase | Status | Duration | Notes |
|-------|--------|----------|-------|
| 1 | completed | 9s | all V4 analysis artifacts confirmed |
| 2 | completed | 14s | adaptation + blueprint confirmed, human gate required |
| 3 | completed | 6s | draft confirmed |
| 4 | completed | 45s | `review.md` + `quality-report.json` + `diff.md`, gate PASS |
| 5 | completed | 9s | final package + `story.yaml`, final validator PASS |

## Validator Results

- `validate-quality-report.py --require-pass`: pass
- `validate-story.py --phase final`: pass
- `check-style-metrics.py --json`: hard forbidden hits `{}`, soft forbidden hits `{}`
- final metrics: 267 non-space chars, average sentence length 16.867, dialogue ratio 0.1948, physical marker `手心: 1`

## Observations

1. V4 mandatory artifact checks behaved correctly; missing-file bypass did not occur.
2. The structured quality gate used `--require-pass` and allowed Phase 5 only after `gate_status=pass`.
3. Phase 5 reran the quality gate before finalizer, which is useful but appears twice in logs.
4. `execution-summary.md` is readable and captures real model label, duration, retry count, prompt and notes.
5. The smoke story is intentionally tiny, so it validates mechanics, not commercial narrative quality.

## Open Problems

1. Auto mode needs a safe execution path for local-only copyrighted sources, probably either a local model mode, a redacted-source test mode, or explicit user-approved external transfer.
2. Manual mode should probably detect non-TTY earlier and print a clearer message.
3. A true quality/effectiveness test still needs an LLM generation pass on a permitted source, because this local smoke test pre-created artifacts.
