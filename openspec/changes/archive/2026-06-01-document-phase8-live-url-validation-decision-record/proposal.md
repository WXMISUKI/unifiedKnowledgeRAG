## Why

Phase 8 now has execution contract, readiness export, and consistency smoke, but we still need one explicit decision record that freezes this cycle's live URL validation verdict and open gates. Without it, reviewers may misread `review` posture as either blocked failure or implicit promotion approval.

## What Changes

- Add a Phase 8 live URL validation decision record under `docs/operations/live-url-validation/`.
- Record evidence basis, current verdict, open gates, and next-step entry conditions.
- Keep this slice documentation-only with no runtime or API behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: adds a traceable Phase 8 live-url decision checkpoint.
- `knowledge-provider`: documents current live-url posture and promotion boundary.

## Impact

- Affected docs: one decision record markdown plus roadmap/progress updates.
- No runtime behavior changes, no deployment behavior changes, no API changes.
