## Why

Phase 3 promotion review still benefits from a slightly broader set of customer-like gate cases. The current canonical benchmark is already strong, but it can use one more small increment of borderline support phrasing, identifier noise, and unsupported empty-trap coverage before we ask anyone to treat the evidence as promotion-ready.

## What Changes

- Add a small, bounded v2 set of customer-like benchmark cases to `tests/fixtures/retrieval_benchmark_cases.json`.
- Keep the additions focused on promotion-risk coverage:
  - one policy-nuance support case
  - one identifier-noise support case
  - one expected-empty false-positive trap
- Refresh the Chinese-seed benchmark evidence generated from the updated fixture.
- Update focused retrieval benchmark assertions and progress notes to match the new fixture shape.

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
