## Context

Phase 3 promotion is still review-only. We already have baseline customer-like coverage, but the promotion readout improves when the fixture has one more small increment of support-like phrasing that mirrors real reviewer questions without changing runtime defaults.

## Goals / Non-Goals

**Goals**

- Add a bounded v2 set of customer-like benchmark cases that improve promotion-review coverage.
- Keep the benchmark deterministic and easy to refresh locally.
- Refresh downstream evidence so handoff and readiness reports stay in sync with the fixture.

**Non-Goals**

- Changing retrieval runtime defaults.
- Introducing new retrieval backends, rerankers, or GraphRAG execution.
- Modifying provider HTTP contracts or control-plane responsibilities.
- Using fixture expansion as a promotion decision by itself.

## Decisions

- Keep using the canonical baseline fixture: `tests/fixtures/retrieval_benchmark_cases.json`.
- Add only a few cases so the change remains easy to review and does not blur the existing Phase 3 gate surface.
- Bias the new cases toward support-like promotion-review prompts that exercise policy nuance, identifier noise, and unsupported empty-trap behavior.
- Refresh the Chinese-seed baseline and dependent review artifacts together so the evidence chain stays current.

## Risks / Trade-offs

- The fixture summary totals will change, so assertions and exported evidence must be refreshed together.
- A slightly larger fixture increases the chance of exposing a new false-positive or false-negative pattern; that is acceptable and should be treated as evidence, not regression noise.
