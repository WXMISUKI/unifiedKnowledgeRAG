## Why

The provider now has a useful handoff bundle, but that bundle reads prerequisite evidence files that may become stale after configuration, dependency, source, or index lifecycle changes. Operators currently need to remember the correct export order manually.

This change adds a lightweight local refresh command that regenerates the existing provider integration and operations evidence in the right order, then rebuilds the handoff bundle. It keeps Phase 6 practical without adding runtime APIs, production workers, provider registration, or GraphRAG execution.

## What Changes

- Add a local handoff evidence refresh workflow that runs the existing evidence exporters in a fixed order.
- Produce a JSON and Markdown refresh summary under `docs/integration/provider-handoff-refresh/`.
- Refresh prerequisite evidence artifacts before refreshing `provider-handoff-bundle-v1`.
- Keep the workflow local and side-effect bounded to evidence files.

## Impact

- Affected specs:
  - `knowledge-provider`: add a local handoff evidence refresh command.
  - `provider-roadmap`: Phase 6 evidence can include a refresh workflow for handoff artifacts.
- Affected code:
  - New refresh service and export CLI.
- Affected docs/evidence:
  - README, lightweight roadmap, generated refresh report.

## Non-Goals

- No new HTTP endpoint.
- No provider registration, heartbeat, audit, or source-to-agent binding behavior.
- No ingestion job creation, explicit reindex execution, model download, vector database call, retrieval query, answer composition, or graph execution beyond the existing local contract smoke behavior.
- No runtime promotion of Qdrant, BGE-M3, hybrid retrieval, reranking, answer composer, or GraphRAG.
