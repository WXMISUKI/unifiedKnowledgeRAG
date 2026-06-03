## Why

Phase 12d established a live pgvector probe report, but the default local environment still does not provide a reproducible path to run that probe. We need one narrow, evidence-backed slice that packages the local pgvector environment itself so the live probe can be executed intentionally rather than left blocked by missing setup.

This change is needed now because the project already knows what it wants to verify from pgvector. The next useful step is to make the local environment explicit: optional driver dependency, isolated compose profile, init SQL, and a runbook that keeps the probe read-only and candidate-only.

## What Changes

- Add a Phase 12e pgvector local probe environment readiness contract that remains provider-first and evaluation-only.
- Add a local environment package that documents the optional pgvector dependency, compose profile, init SQL, and setup runbook.
- Keep the existing provider contract, `evidence_pack-v1`, and runtime defaults unchanged.
- Keep pgvector as a candidate backend only; do not promote it to the default runtime backend in this change.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `provider-roadmap`: add a Phase 12e local probe environment checkpoint and keep it explicitly provider-first and evaluation-only.
- `retrieval-benchmark-harness`: add a shared local-environment evidence/export contract so pgvector setup can be reviewed with the same decision states as earlier candidate readiness slices.

## Impact

- Adds a new local evidence/reporting slice under `docs/operations/pgvector-local-probe-environment/`.
- Adds a pgvector optional dependency file, compose example, and init SQL under the repo root.
- Adds a pgvector local environment readiness service and export script under `app/services/` and `scripts/`.
- Adds optional handoff/refresh visibility for the new review artifact.
- No default runtime backend change, no caller-control-plane change, and no GraphRAG or parser expansion work.
