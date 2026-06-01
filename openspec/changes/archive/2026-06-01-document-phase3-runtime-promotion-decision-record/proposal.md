## Why

Phase 3 now has multiple candidate-level exports and smokes, but we still need a single decision record that explicitly captures the current runtime promotion verdict. Without this record, reviewers may over-interpret isolated candidate wins and miss the agreed "evaluation-only, no default promotion" boundary.

## What Changes

- Add a Phase 3 runtime promotion decision record under `docs/benchmark/chinese-seed/runtime-promotion-decision/`.
- Record evidence basis, open gates, and explicit decision to keep current runtime defaults.
- Keep this change documentation-only; no runtime/config/API behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: adds a traceable decision record for Phase 3 promotion posture.
- `retrieval-benchmark-harness`: documents the promotion verdict over current evidence set.

## Impact

- Affected docs: one decision record markdown plus tracker refresh.
- No code-path, deployment, or API impact.
