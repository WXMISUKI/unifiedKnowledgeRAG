## Why

The provider now has a mature local ingestion lifecycle, but production indexing requires architectural choices that affect cost, deployment, data governance, retrieval quality, and operations. Decisions such as embedding model, vector database, hybrid retrieval, reranker, and graph storage should be evaluated and confirmed before implementation.

## What Changes

- Add a production indexing architecture decision document.
- Define decision criteria for embedding model, vector database, queue/worker runtime, chunking, reranking, and GraphRAG storage.
- Record candidate options and trade-offs without prematurely selecting a final vendor or model.
- Add a decision gate that blocks production dependency implementation until the open decisions are reviewed.
- Update README and project docs to point future implementation work through this decision record.

## Capabilities

### New Capabilities

- `production-indexing-architecture`: Architecture decision process and readiness requirements for production-grade indexing infrastructure.

### Modified Capabilities

- `knowledge-provider`: Provider documentation must identify production indexing decisions as explicit, reviewable architecture choices.
- `index-lifecycle`: Production queue/worker implementation must follow the architecture decision record instead of extending the local runner ad hoc.

## Impact

- Adds `docs/architecture/production_indexing_architecture.md`.
- Adds OpenSpec requirements for decision gates and production indexing readiness.
- Updates README with the decision workflow.
- Does not add external dependencies, queue infrastructure, vector database clients, or embedding model integrations in this slice.
