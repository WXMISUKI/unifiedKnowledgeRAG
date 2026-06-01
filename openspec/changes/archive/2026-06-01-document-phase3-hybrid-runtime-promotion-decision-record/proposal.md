## Why

Phase 3 now has hybrid runtime promotion contract, readiness export, and smoke evidence, but still needs a final decision record that captures the current verdict in one place. Without this record, reviewers can misread candidate readiness as an approved default promotion.

## What Changes

- Add a Phase 3 hybrid runtime promotion decision record under `docs/benchmark/chinese-seed/hybrid-runtime-promotion/`.
- Record current verdict, evidence basis, open gates, and promotion preconditions.
- Keep this change documentation-only; no runtime/config/API behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: adds a traceable final decision record for hybrid runtime promotion posture.
- `retrieval-benchmark-harness`: documents promotion verdict over current hybrid decision evidence chain.

## Impact

- Affected docs: one decision record markdown plus tracker refresh.
- No code-path, deployment, or API impact.
