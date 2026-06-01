## Why

Phase 7 now has acceptance contract, release-readiness export, and cross-phase consistency smoke, but we still need one explicit decision record that captures this cycle's release verdict. Without it, reviewers may over-interpret local handoff readiness as runtime promotion approval.

## What Changes

- Add a Phase 7 provider release decision record under `docs/operations/provider-release-readiness/`.
- Record evidence basis, current verdict, open gates, and next-step entry conditions.
- Keep this slice documentation-only with no runtime or API behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: adds a traceable Phase 7 cross-phase release verdict checkpoint.
- `knowledge-provider`: documents the current local-handoff vs runtime-promotion decision boundary.

## Impact

- Affected docs: one decision record markdown plus roadmap/progress updates.
- No runtime behavior changes, no deployment behavior changes, no API changes.
