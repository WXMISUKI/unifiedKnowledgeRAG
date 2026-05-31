## Why

Phase 3 FP/FN review evidence is available, but external reviewers still need to open it outside the provider handoff chain. This adds lightweight visibility without changing runtime defaults.

## What Changes

- Add optional `phase3_fp_fn_review` artifact to provider handoff bundle.
- Summarize FP/FN metrics in handoff artifact summary.
- Add a non-blocking handoff refresh step that regenerates FP/FN review evidence.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: handoff evidence includes optional Phase 3 FP/FN review summary.
- `provider-roadmap`: records this as Phase 3/Phase 6 evidence visibility work.

## Impact

- Affected code: `app/services/provider_handoff_bundle.py`, `app/services/provider_handoff_refresh.py`
- Affected tests: `tests/test_provider_handoff_bundle.py`, `tests/test_provider_handoff_refresh.py`
- No runtime retrieval default changes, no API contract changes
