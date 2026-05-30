## Why

Source document manifests now expose local file fingerprint and drift diagnostics, but reindex readiness still only considers file presence, index status, and job history. If a source file has changed while the index status still says ready, operators should see that reindexing is recommended before handing evidence to MyPrivateAgent or promoting a deployment.

This change connects Phase 2 source freshness diagnostics to Phase 6 reindex planning without adding ingestion automation or changing retrieval behavior.

## What Changes

- Include source document drift summaries in `reindex-readiness-v1`.
- Recommend reindex when a source document reports `drift_status=changed`.
- Preserve blocked behavior for missing source files and review behavior for unchecked fingerprint diagnostics.
- Keep the report read-only and side-effect free.

## Impact

- Affected specs:
  - `index-lifecycle`: reindex readiness uses source fingerprint drift diagnostics.
  - `provider-roadmap`: Phase 2 freshness evidence can inform Phase 6 operations evidence.
- Affected code:
  - Reindex readiness service and Markdown/JSON report shape.
- Affected docs/evidence:
  - README, roadmap, regenerated reindex readiness and handoff evidence where applicable.

## Non-Goals

- No automatic ingestion job creation.
- No index rebuild execution.
- No retrieval default changes.
- No embedding, Qdrant, reranker, answer composer, or GraphRAG changes.
