## Why

Phase 6 now has Qdrant contract and readiness export, but there is still no compact smoke artifact that checks whether backup/restore review prerequisites are currently satisfied. Reviewers need a repeatable local smoke summary before private-network promotion review.

## What Changes

- Add a local Phase 6 Qdrant backup/restore smoke summary export.
- Validate contract, readiness export, and deployment/reindex posture in one read-only smoke report.
- Wire optional smoke evidence into provider handoff and handoff refresh.
- Keep this slice side-effect free; no real backup/restore execution.

## Capabilities

### New Capabilities

- `phase6-qdrant-backup-restore-smoke`: read-only smoke summary for Qdrant backup/restore prerequisites.

### Modified Capabilities

- `knowledge-provider`: handoff bundle and refresh can summarize optional Qdrant backup/restore smoke evidence.
- `provider-roadmap`: records Qdrant backup/restore smoke as Phase 6 operations evidence maintenance.

## Impact

- Affected code: new smoke service/export script and handoff integrations.
- Affected tests: focused smoke and handoff assertions.
- Runtime defaults and API contracts remain unchanged.
