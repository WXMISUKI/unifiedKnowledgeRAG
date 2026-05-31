## Why

The Phase 4 evidence pack consumption contract and readiness export are both in place, but we still lack a small executable smoke that proves a caller can consume `evidence_pack-v1` correctly in the two most important branches: answerable evidence and fail-closed insufficient evidence.

## What Changes

- Add a local Phase 4 caller-consumption smoke export that writes JSON and Markdown evidence files.
- Validate the caller-facing `evidence_pack-v1` rules directly through the shared evidence-pack helper rather than rechecking provider HTTP flow.
- Surface the smoke through provider handoff and handoff refresh as optional review evidence.
- Keep the smoke read-only. It should confirm caller consumption semantics, not change runtime behavior or provider scope.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds an exportable Phase 4 caller-consumption smoke report.
- `knowledge-provider`: provider handoff and refresh can summarize the new smoke as optional evidence.
- `provider-roadmap`: records the smoke as lightweight Phase 4 evidence packaging work.

## Impact

- Affected code: `app/services/phase4_caller_consumption_smoke.py` (new), `scripts/export_phase4_caller_consumption_smoke.py` (new)
- Affected tests: `tests/test_phase4_caller_consumption_smoke.py` (new), plus focused handoff bundle/refresh assertions
- Affected docs/evidence: `docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json` and `.md`
- No runtime default changes, no new HTTP API, no new dependencies
