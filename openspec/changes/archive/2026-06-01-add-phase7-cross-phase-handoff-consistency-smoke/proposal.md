## Why

Phase 7 release-readiness export gives a cross-phase summary, but reviewers still need a compact smoke check that validates consistency across key phase decisions and readiness/smoke artifacts. Without this smoke, cross-phase drift can hide behind individually green reports.

## What Changes

- Add a local Phase 7 cross-phase handoff consistency smoke report under `docs/smoke/cross-phase-handoff/`.
- Validate alignment across:
  - Phase 7 release-readiness decision
  - Phase 2 parser decision record
  - Phase 3 runtime decision record
  - Phase 4 caller-consumption smoke
  - Phase 5 graph boundary smoke
  - Phase 6 deployed field-validation readiness
- Include this smoke in provider handoff bundle and handoff refresh as optional evidence.
- Keep this slice read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: handoff bundle/refresh can summarize optional Phase 7 cross-phase consistency smoke.
- `provider-roadmap`: records Phase 7 cross-phase consistency visibility work.

## Impact

- Affected code: new Phase 7 smoke service/export script and handoff integration.
- Affected tests: new smoke tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local Phase 7 cross-phase smoke JSON and Markdown artifacts.
- Runtime defaults remain unchanged.
