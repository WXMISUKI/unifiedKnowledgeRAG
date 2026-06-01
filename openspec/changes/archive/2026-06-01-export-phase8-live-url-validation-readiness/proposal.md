## Why

Phase 8 now has an execution contract, but reviewers still need one machine-readable readiness export to interpret live URL validation posture from existing Phase 6/Phase 7/deployed-smoke evidence.

## What Changes

- Add a local Phase 8 live URL validation readiness export under `docs/operations/live-url-validation/`.
- Summarize contract presence, Phase 6 field-validation posture, Phase 7 release posture, and deployed smoke evidence in one report.
- Include this Phase 8 readiness export in provider handoff bundle and handoff refresh as optional review evidence.
- Keep this change read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: handoff bundle/refresh can summarize optional Phase 8 live URL validation readiness evidence.
- `provider-roadmap`: records Phase 8 readiness visibility work.

## Impact

- Affected code: new Phase 8 readiness service/export script and handoff integration.
- Affected tests: new readiness tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local Phase 8 readiness JSON and Markdown artifacts.
- Runtime defaults remain unchanged.
