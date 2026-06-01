## Why

Phase 6 now has a Qdrant operations contract, but reviewers still need to manually combine deployment readiness, reindex posture, and existing Qdrant benchmark artifacts. A machine-readable export is needed so promotion review can consume one consistent evidence surface.

## What Changes

- Add a local `phase6-qdrant-vector-store-readiness` export (JSON + Markdown).
- Summarize deployment, backup/recovery contract presence, reindex linkage, and Qdrant candidate benchmark posture.
- Wire this export into provider handoff bundle and handoff refresh as optional evidence.
- Keep everything read-only and evaluation-only.

## Capabilities

### New Capabilities

- `phase6-qdrant-vector-store-readiness`: local operations readiness export for Qdrant deployment and recovery evidence review.

### Modified Capabilities

- `knowledge-provider`: handoff bundle and refresh can summarize optional Qdrant vector-store readiness evidence.
- `provider-roadmap`: records Qdrant vector-store readiness export as Phase 6 evidence visibility work.

## Impact

- Affected code: new readiness service/export script, handoff bundle parser, handoff refresh step list.
- Affected tests: focused unit coverage for readiness export and handoff integration.
- Runtime defaults and public APIs remain unchanged.
