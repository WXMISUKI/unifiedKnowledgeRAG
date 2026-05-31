## Why

Current benchmark evidence is strong for seed and candidate gates, but Phase 3 promotion still lacks enough customer-like false-positive and false-negative coverage. We need a small expansion that improves decision confidence without changing runtime defaults.

## What Changes

- Add a small customer-like benchmark fixture pack focused on borderline support questions, identifier noise, and expected-empty traps.
- Keep this fixture as evaluation-only evidence used by benchmark export workflows.
- Extend focused benchmark tests to assert fixture loading and category summaries.
- Do not change retrieval runtime defaults, provider contracts, or promotion gates.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: benchmark fixtures and evidence now include additional customer-like gate cases.
- `provider-roadmap`: records this as lightweight Phase 3 evidence expansion, not runtime promotion.

## Impact

- Affected fixtures: benchmark case JSON under `tests/fixtures`.
- Affected tests: focused retrieval benchmark fixture/category assertions.
- Affected evidence workflow: benchmark export inputs become more representative.
- No API contract or runtime dependency changes.
