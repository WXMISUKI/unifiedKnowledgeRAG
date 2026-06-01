## Why

Phase 6 already has deployment and reindex readiness exports, but Qdrant vector-store operations are still spread across generic notes. Reviewers do not yet have a single contract that states what "deployment/backup/recovery ready" means for Qdrant in this lightweight provider, especially under private-network promotion review.

## What Changes

- Add a local Phase 6 contract document for Qdrant deployment, backup, and recovery readiness.
- Define required evidence fields, review gates, and non-goals for Qdrant operations.
- Keep this slice documentation-only: no runtime default changes, no automatic restore, no deployment automation.

## Capabilities

### New Capabilities

- `qdrant-vector-store-readiness`: documentation contract for Qdrant deployment/backup/recovery evidence in Phase 6.

### Modified Capabilities

- `provider-roadmap`: records Qdrant deployment/backup/recovery readiness as Phase 6 operations evidence.
- `knowledge-provider`: records provider-owned Qdrant readiness evidence boundary (read-only, operator-facing, non-control-plane).

## Impact

- Affected docs: `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-deployment-backup-recovery-contract.md`.
- Affected specs: `provider-roadmap`, `knowledge-provider`.
- Runtime behavior, retrieval defaults, and APIs remain unchanged.
