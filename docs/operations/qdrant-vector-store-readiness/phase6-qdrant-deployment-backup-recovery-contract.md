# Phase 6 Qdrant Deployment/Backup/Recovery Contract

## Scope

- Phase: `Phase 6 / Deployment And Operations`
- Type: read-only operations readiness contract
- Goal: define Qdrant deployment/backup/recovery evidence requirements before any runtime promotion review

## Non-goals

- Do not switch runtime retrieval default to `qdrant`.
- Do not trigger backup, restore, reindex, or deployment automation.
- Do not move control-plane governance, approval, audit, or registration ownership into this provider.

## Required Evidence

### 1) Deployment Posture

- `qdrant_url` and network posture (local/private-network/public ingress) are documented.
- `qdrant_collection`, `qdrant_vector_name`, and vector size compatibility are documented.
- Secret-handling posture is documented: API key presence is visible, secret value remains redacted.
- Provider-side dependency posture is documented (client package/version and expected connectivity checks).

Recommended action when missing: `review_qdrant_deployment_config`.

### 2) Backup Posture

- Snapshot/export path convention is documented (who runs it, where it lands, how it is named).
- Retention and rotation expectation is documented (lightweight policy statement is enough).
- Checksum/manifest expectation for snapshot artifacts is documented.
- Private-network copy/reuse posture is documented.

Recommended action when missing: `document_qdrant_backup_policy`.

### 3) Recovery Posture

- Restore drill evidence expectation is documented (at least one reproducible drill plan).
- Restore success criteria are documented (collection visible, query path healthy, citation path still valid).
- Failure handling expectation is documented (rollback/rebuild path, escalation owner).
- Reindex linkage is documented (when to restore snapshot vs when to rebuild from source).

Recommended action when missing: `prepare_qdrant_restore_drill`.

## Readiness States

- `ready`: deployment, backup, and recovery evidence are all present and internally consistent.
- `review`: evidence exists but has open review gates, or environment is still mock/fixture.
- `blocked`: critical deployment or recovery prerequisites are missing or contradictory.

## Promotion Boundary

This contract is prerequisite evidence for later `Qdrant + BGE-M3` private-network promotion review. It is not a promotion decision artifact. Runtime defaults remain unchanged until benchmark quality, FP/FN review, latency/resource posture, and deployed smoke gates are approved.
