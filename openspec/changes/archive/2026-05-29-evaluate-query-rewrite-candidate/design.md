# Design: Query Rewrite Candidate Evaluation

## Candidate Shape

Each query rewrite candidate has:

- `id`
- `description`
- `implementation_status`
- `rewrite_policy`
- `risk_notes`

The first candidates are:

- `original-query-baseline`: no rewrite, baseline.
- `controlled-support-rewrite-v1`: deterministic rewrite rules for known Chinese support shorthand and paraphrase cases.

## Rewrite Rules

This slice intentionally uses deterministic local rules instead of an LLM. The goal is to prove the evaluation surface, not to approve a production rewriting model.

Rules should:

- Only rewrite known non-empty benchmark cases.
- Avoid rewriting expected-empty cases.
- Preserve source ids, expected citation, category, and difficulty.
- Keep original and rewritten query visible in evidence.

## Metrics

Evidence includes:

- Candidate metadata.
- Total cases.
- Rewritten case count.
- Rewrite rate.
- Expected-empty rewrite count.
- Benchmark summary metrics after rewrite.
- Per-case original query, rewritten query, rewrite flag, and retrieval outcome.

## Runtime Boundary

This change does not modify `/api/rag/retrieve`, Qdrant runtime retrieval, or default backend behavior. Query rewrite remains a local evidence workflow.

## Validation

- Focused tests for rewrite rules and export shape.
- Full pytest suite.
- OpenSpec strict validation.
