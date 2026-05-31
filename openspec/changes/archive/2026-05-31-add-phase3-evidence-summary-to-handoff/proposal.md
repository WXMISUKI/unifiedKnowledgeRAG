## Why

Phase 3 benchmark evidence is refreshed and useful, but handoff bundle reviewers still need to open benchmark files separately. Adding a compact read-only summary row in handoff reduces review friction and keeps evidence discovery in one place.

## What Changes

- Add a Phase 3 seed evidence artifact row to provider handoff bundle.
- Summarize key metrics from the refreshed fixture baseline evidence:
  `total_cases`, `hit_rate`, `citation_match_rate`, `empty_handling_rate`.
- Keep this artifact optional and read-only.
- Do not change runtime retrieval defaults, provider contracts, or promotion gates.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: provider handoff evidence includes a compact Phase 3 retrieval evidence summary row.
- `provider-roadmap`: records the addition as lightweight Phase 3/Phase 6 review ergonomics, not runtime promotion.

## Impact

- Affected code: `app/services/provider_handoff_bundle.py`
- Affected tests: `tests/test_provider_handoff_bundle.py`
- Affected docs/evidence rendering: handoff JSON/Markdown output
- No API path changes, no retrieval behavior changes, no new dependencies
