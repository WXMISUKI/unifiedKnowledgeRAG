## Context

The project now exports local Phase 3 FP/FN review evidence. To keep handoff review one-stop and lightweight, the artifact should be visible from handoff bundle and refresh workflow.

## Goals / Non-Goals

**Goals**

- Surface compact FP/FN metrics in handoff evidence.
- Keep FP/FN artifact optional and non-blocking.
- Regenerate FP/FN evidence during handoff refresh without turning refresh brittle.

**Non-Goals**

- No retrieval strategy change.
- No runtime promotion or gating policy changes.
- No new public HTTP API.

## Decisions

- Add optional handoff artifact `phase3_fp_fn_review`.
- Parse `false_positive_count`, `false_negative_count`, `false_positive_rate`, `false_negative_rate`.
- Add refresh step `phase3_fp_fn_review` that degrades to `review` on missing source evidence instead of hard-blocking.

## Risks / Trade-offs

- FP/FN review depends on existing benchmark evidence; missing input should be reviewable, not blocking.
- More handoff rows are acceptable for better reviewer ergonomics.
