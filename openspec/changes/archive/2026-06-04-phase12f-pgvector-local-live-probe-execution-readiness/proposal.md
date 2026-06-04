## Why

Phase 12e packaged the optional local pgvector environment, but the project still lacks an explicit, reviewable slice for the actual local live-probe rerun path. We need one narrow evidence-backed step that says when the environment is ready to execute the Phase 12d live probe locally, without implying runtime promotion.

## What Changes

- Add a Phase 12f pgvector local live-probe execution readiness contract that stays provider-first and evaluation-only.
- Add a local execution runbook and exported readiness artifact that record the rerun path, current Phase 12d status, and handoff visibility.
- Keep the existing provider contract, `evidence_pack-v1`, and runtime defaults unchanged.
- Keep pgvector candidate-only; do not promote it to a runtime default in this change.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `provider-roadmap`: add a Phase 12f local live-probe execution readiness checkpoint and keep it explicitly provider-first and evaluation-only.
- `retrieval-benchmark-harness`: add a shared local execution-evidence contract so the Phase 12d rerun path can be reviewed with the same decision vocabulary as earlier candidate readiness slices.

## Impact

- Adds a new local execution evidence/reporting slice under `docs/operations/pgvector-local-live-probe-execution/`.
- Adds a pgvector local live-probe execution readiness service and export script under `app/services/` and `scripts/`.
- Adds optional handoff/refresh visibility for the new review artifact.
- No default runtime backend change, no caller-control-plane change, and no GraphRAG or parser expansion work.
