## Why

The benchmark fixture has been expanded to 24 customer-like cases, but Phase 3 seed evidence exports can lag behind fixture updates if reports are not regenerated. We need a small evidence refresh slice so review artifacts match current benchmark inputs.

## What Changes

- Regenerate Phase 3 Chinese-seed retrieval candidate evidence after fixture expansion.
- Regenerate related benchmark candidate evidence files that depend on the baseline fixture.
- Update progress tracking notes to record refreshed evidence status and paths.
- Keep all changes evidence-only; do not change runtime retrieval defaults or provider contracts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: exported seed evidence stays synchronized with the current canonical benchmark fixture.
- `provider-roadmap`: records this as Phase 3 evidence maintenance, not runtime promotion.

## Impact

- Affected docs: `docs/benchmark/chinese-seed/**` reports
- Affected tracking: `docs/progress/provider-improvement-tracker.md`
- No API changes, no backend default changes, no new dependencies
