## Why

Phase 6 already has a deployed field-validation readiness export and a deployed provider smoke report, but reviewers still have to mentally compare the readiness artifact and provider handoff bundle to understand whether the live-url posture is internally consistent. We need a compact, read-only smoke summary that validates the handoff view without introducing any live network calls.

## What Changes

- Add a local Phase 6 deployed handoff consistency smoke summary that compares the deployed field-validation readiness export with the provider handoff bundle.
- Summarize whether the readiness status, live-url posture, and open-gate posture remain aligned across the two local artifacts.
- Surface the smoke summary through provider handoff and handoff refresh as optional review evidence.
- Keep the smoke read-only. It should inspect local evidence only and must not run live deployed provider requests.

## Capabilities

### New Capabilities

- `deployed-field-validation-consistency-smoke`: read-only consistency smoke for deployed field-validation readiness and handoff bundle posture.

### Modified Capabilities

- `provider-roadmap`: records the smoke as lightweight Phase 6 operations evidence.
- `knowledge-provider`: provider handoff and refresh can summarize the new deployed field-validation consistency smoke evidence as optional evidence.
- `retrieval-benchmark-harness`: adds an exportable deployed handoff consistency smoke report.

## Impact

- Affected code: `app/services/phase6_deployed_handoff_consistency_smoke.py` (new), `scripts/export_phase6_deployed_handoff_consistency_smoke.py` (new)
- Affected tests: `tests/test_phase6_deployed_handoff_consistency_smoke.py` (new), plus focused handoff bundle/refresh assertions
- Affected docs/evidence: `docs/smoke/deployed-field-validation/phase6-deployed-handoff-consistency-smoke.json` and `.md`
- No runtime default changes, no new HTTP API, no new dependencies
