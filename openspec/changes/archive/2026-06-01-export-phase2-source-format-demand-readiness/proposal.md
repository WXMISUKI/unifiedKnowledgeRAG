## Why

Phase 2 already has a parser-expansion demand contract, but reviewers still need a machine-readable readiness snapshot that summarizes current source-format demand signals from real local evidence. Without this export, parser-expansion review remains spread across source-binding rows and ad-hoc reading.

## What Changes

- Add a local Phase 2 source-format demand readiness export under `docs/operations/source-format-demand/`.
- Summarize markdown baseline posture, unsupported/non-markdown demand signals, and open expansion gates in one report.
- Include this report in provider handoff bundle and handoff refresh as optional read-only evidence.
- Keep this slice evaluation-only and do not enable non-Markdown runtime parsing.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records this as Phase 2 ingestion evidence visibility work.
- `knowledge-provider`: handoff bundle/refresh can summarize Phase 2 source-format demand readiness as optional evidence.

## Impact

- Affected code: new Phase 2 readiness service and export script.
- Affected tests: new readiness tests and focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown readiness artifacts.
- Runtime defaults remain unchanged.
