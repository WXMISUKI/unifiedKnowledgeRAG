## Context

Phase 3 promotion is evidence-gated. The current benchmark fixture is already useful, but promotion-review confidence improves when the seed set includes a few more customer-like phrases that are close to real support traffic while still remaining deterministic and lightweight.

## Goals / Non-Goals

**Goals**

- Add a bounded number of customer-like benchmark cases to improve promotion review coverage.
- Keep the benchmark deterministic and easy to refresh locally.
- Refresh downstream evidence so handoff and readiness reports stay in sync with the fixture.

**Non-Goals**

- Changing retrieval runtime defaults.
- Introducing new retrieval backends, rerankers, or GraphRAG execution.
- Modifying provider HTTP contracts or control-plane responsibilities.
- Using fixture expansion as a promotion decision by itself.

## Decisions

- Keep using the canonical baseline fixture: `tests/fixtures/retrieval_benchmark_cases.json`.
- Prefer cases that reuse the current refund/logistics evidence surface, because those are already exercised by the existing benchmark harness and handoff bundle.
- Keep the addition small so summary churn stays reviewable and the refresh cost remains low.

## Risks / Trade-offs

- The fixture summary totals will change, so assertions and exported evidence must be refreshed together.
- A slightly larger fixture increases the chance of exposing a new false-positive or false-negative pattern; that is acceptable and should be treated as evidence, not regression noise.
