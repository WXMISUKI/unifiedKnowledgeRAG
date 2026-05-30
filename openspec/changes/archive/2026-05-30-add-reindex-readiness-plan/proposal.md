## Why

Deployment readiness now summarizes provider health and configuration, but operators still need a read-only reindex plan before refreshing source indexes in local or private-network deployments. This advances roadmap Phase 6 without adding new infrastructure or mutating indexes.

## What Changes

- Add a local reindex readiness plan report for configured knowledge sources.
- Summarize source file presence, current index status, latest ingestion job, job counts, and recommended reindex action.
- Export machine-readable JSON and reviewable Markdown under `docs/operations/reindex-readiness/`.
- Keep the report read-only: it does not start ingestion jobs, clear indexes, call embeddings, call Qdrant, or rebuild indexes.

## Capabilities

### New Capabilities

### Modified Capabilities
- `index-lifecycle`: Source index lifecycle can be inspected as a local reindex readiness plan before operators trigger rebuilds.
- `provider-roadmap`: Phase 6 operations evidence includes reindex planning without moving deployment governance into the provider.

## Impact

- Affected code: new reindex readiness service and export CLI.
- Affected docs/evidence: README, roadmap, generated reindex readiness report.
- API compatibility: no HTTP API changes.
- Dependencies: none.
