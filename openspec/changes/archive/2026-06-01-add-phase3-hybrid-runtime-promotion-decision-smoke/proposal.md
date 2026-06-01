## Why

After adding the hybrid runtime promotion decision readiness export, we still need a compact smoke that validates final decision evidence-chain completeness in one place. Without this smoke, missing or malformed prerequisites may be discovered late during review.

## What Changes

- Add a local Phase 3 hybrid runtime promotion decision smoke report.
- Validate contract, readiness export, and key Phase 3/Phase 6 bridge evidence presence and JSON parseability.
- Export JSON and Markdown smoke artifacts under `docs/smoke/hybrid-runtime-promotion/`.
- Surface this smoke as optional review evidence in provider handoff bundle and handoff refresh.
- Keep the smoke read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds exportable Phase 3 hybrid runtime promotion decision smoke evidence.
- `knowledge-provider`: handoff bundle/refresh can summarize this smoke as optional Phase 3 evidence.
- `provider-roadmap`: records this as lightweight Phase 3 evidence maintenance work.

## Impact

- Affected code: new smoke service and export script.
- Affected tests: new smoke tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: new smoke artifacts and tracker/roadmap references.
- Runtime defaults and promotion decisions remain unchanged.
