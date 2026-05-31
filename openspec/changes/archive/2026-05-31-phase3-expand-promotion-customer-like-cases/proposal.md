## Why

Phase 3 promotion still depends on customer-like retrieval evidence, but the canonical benchmark fixture is still a bit thin on borderline support phrasing, noisy identifiers, and expected-empty traps that are close to real support traffic. We want a small, reviewable expansion that increases decision confidence without changing runtime defaults.

## What Changes

- Add a small number of customer-like benchmark cases to `tests/fixtures/retrieval_benchmark_cases.json`.
- Keep the new cases focused on promotion-risk coverage such as noisy identifiers, policy nuance phrasing, and expected-empty traps.
- Refresh the Chinese-seed benchmark evidence generated from the updated fixture.
- Update the focused retrieval benchmark assertions and progress notes to match the new fixture shape.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: customer-like benchmark coverage becomes slightly broader for Phase 3 promotion review.
- `provider-roadmap`: records the expansion as evidence-only Phase 3 work, not runtime promotion.

## Impact

- Affected fixtures: `tests/fixtures/retrieval_benchmark_cases.json`
- Affected tests: `tests/test_retrieval_benchmark.py`
- Affected evidence: `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.{json,md}`
- Affected review artifacts: FP/FN review and retrieval promotion readiness export refresh outputs
- No API contract changes and no runtime default changes
