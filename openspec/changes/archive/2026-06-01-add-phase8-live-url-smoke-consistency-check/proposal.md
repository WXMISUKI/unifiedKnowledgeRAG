## Why

After Phase 8 readiness export exists, reviewers still need one compact consistency check to verify that handoff bundle summaries stay aligned with the readiness report and do not drift.

## What Changes

- Add a local Phase 8 live URL smoke consistency check under `docs/smoke/live-url-validation/`.
- Compare Phase 8 readiness summary fields against provider handoff bundle row fields.
- Include this smoke artifact in provider handoff bundle and handoff refresh as optional evidence.
- Keep this change read-only and local.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: handoff bundle/refresh can summarize optional Phase 8 live URL smoke consistency evidence.
- `provider-roadmap`: records Phase 8 readiness-vs-handoff consistency visibility.

## Impact

- Affected code: new Phase 8 smoke service/export script and handoff integration.
- Affected tests: new smoke tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local Phase 8 smoke JSON and Markdown artifacts.
- Runtime defaults remain unchanged.
