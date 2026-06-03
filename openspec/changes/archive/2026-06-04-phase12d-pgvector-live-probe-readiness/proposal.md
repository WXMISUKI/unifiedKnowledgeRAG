## Why

Phase 12c established a configuration-driven pgvector candidate readiness slice, but it still stops short of a real local PostgreSQL probe. We now need one narrow, evidence-backed step that can validate whether a local pgvector deployment is actually reachable, extension-enabled, and structurally aligned with the provider's expected schema shape.

This change is needed now because the project already has a stable provider-first boundary, the pgvector candidate is explicitly isolated from runtime defaults, and the next useful question is no longer "is pgvector configured?" but "can the configured backend actually answer the minimal live probe?"

## What Changes

- Add a Phase 12d pgvector live probe readiness contract that stays provider-first and evaluation-only.
- Add a local readiness export that can optionally validate a live PostgreSQL connection, `vector` extension availability, schema visibility, table visibility, and index visibility.
- Keep the existing provider contract, `evidence_pack-v1`, and runtime defaults unchanged.
- Keep the probe optional and read-only; do not add ingestion, writes, index rebuilds, or runtime promotion in this change.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `provider-roadmap`: add a Phase 12d pgvector live-probe checkpoint that remains optional, reversible, and provider-first.
- `retrieval-benchmark-harness`: add a shared pgvector live-probe evidence/export contract so pgvector can be reviewed with the same decision vocabulary as the earlier candidate readiness slice.

## Impact

- Adds a new local evidence/reporting slice under `docs/operations/pgvector-live-probe-readiness/`.
- Adds a pgvector live probe readiness service and export script under `app/services/` and `scripts/`.
- Adds optional handoff/refresh visibility for the new review artifact.
- No default runtime backend change, no caller-control-plane change, and no GraphRAG or parser expansion work.
