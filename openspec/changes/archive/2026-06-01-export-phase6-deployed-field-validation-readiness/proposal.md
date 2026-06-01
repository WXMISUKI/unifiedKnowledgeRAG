## Why

Phase 6 already has deployment readiness and deployed provider smoke evidence, but reviewers still have to piece together whether a real deployed URL is actually visible as field validation evidence. We need one machine-readable export that makes that review path obvious without adding any deployment automation.

## What Changes

- Add a local Phase 6 deployed field validation readiness export under `docs/operations/deployed-field-validation/`.
- Summarize deployment readiness, handoff bundle posture, and deployed smoke evidence in one review artifact.
- Surface this artifact in provider handoff bundle and handoff refresh as optional review evidence.
- Keep this work read-only and evaluation-only; do not change runtime defaults.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: handoff bundle/refresh can summarize optional deployed field validation readiness evidence.
- `provider-roadmap`: records deployed field validation readiness export as Phase 6 evidence visibility work.

## Impact

- Affected code: new readiness service and export script.
- Affected tests: new readiness tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown readiness artifacts.
- Runtime defaults remain unchanged.
