## Context

`tests/fixtures/retrieval_benchmark_cases.json` now has 24 baseline cases, including customer-like additions. Existing benchmark evidence under `docs/benchmark/chinese-seed/` must be regenerated so gate reviews and roadmap discussions reference current inputs.

This slice should remain lightweight and deterministic: refresh evidence and notes, without changing runtime behavior.

## Goals / Non-Goals

**Goals:**

- Keep seed evidence exports aligned with the canonical fixture.
- Ensure exported totals and category summaries reflect 24 baseline cases.
- Record refreshed status in the progress tracker for ongoing review.

**Non-Goals:**

- Runtime retrieval backend promotion.
- Threshold/hybrid/reranker default changes.
- Provider API contract changes.
- GraphRAG execution changes.

## Decisions

- Reuse existing export commands/services rather than introducing new scripts.
- Treat evidence refresh as a spec-tracked change so archive history remains clear.
- Validate with focused benchmark tests and OpenSpec validation.

## Risks / Trade-offs

- Regenerated reports can differ from prior snapshots -> expected and desirable after fixture change.
- Some candidate reports may expose weaker metrics -> keep as review evidence, not promotion signal by itself.
