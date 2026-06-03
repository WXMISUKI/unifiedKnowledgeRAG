## Why

Phase 12b has already established a review-only candidate backend readiness layer, but `pgvector` is still only a reference-point in the evaluation roadmap. We now need one narrow, evidence-backed spike that can answer whether PostgreSQL-native vector search is worth moving from comparison-only into local candidate review without changing the provider default.

This change is needed now because the existing provider-first path is stable enough to support a focused backend spike, and `pgvector` is the least disruptive way to test operational reuse, schema isolation, backup/recovery posture, and citation stability under the project's lightweight boundary.

## What Changes

- Add a Phase 12c pgvector candidate backend spike readiness contract that remains read-only and provider-first.
- Add a local readiness export that consolidates pgvector-specific evidence and clearly separates configured, reviewable, and blocked states.
- Add a compact smoke and export path that can surface pgvector candidate posture in handoff and refresh evidence.
- Keep the existing provider contract, `evidence_pack-v1`, and runtime defaults unchanged.
- Keep pgvector as a candidate backend only; do not promote it to the default runtime backend in this change.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `provider-roadmap`: add a Phase 12c pgvector candidate backend spike readiness checkpoint and keep it explicitly provider-first and evaluation-only.
- `retrieval-benchmark-harness`: add a shared pgvector candidate evidence/export contract so pgvector can be reviewed with the same decision states as other backend candidates.

## Impact

- Adds a new local evidence/reporting slice under `docs/operations/pgvector-candidate-backend-readiness/`.
- Adds a pgvector candidate readiness service and export script under `app/services/` and `scripts/`.
- Adds optional handoff/refresh visibility for the new review artifact.
- No default runtime backend change, no caller-control-plane change, and no GraphRAG or parser expansion work.
