## Why

unifiedKnowledgeRAG needs a stable provider boundary before implementation so MyPrivateAgent can consume RAG and GraphRAG evidence without depending on vector-store, graph-store, or framework internals.

The first delivery slice should prove the provider contract with document RAG while preserving a clear GraphRAG API boundary for later Neo4j-backed implementation.

## What Changes

- Introduce unified Knowledge Provider v1 as an independent HTTP JSON service.
- Define provider capabilities for health, catalog readiness, document RAG retrieval, and graph query contracts.
- Implement the first runtime slice for document RAG only: health, capabilities, catalog, sources, and retrieve.
- Keep GraphRAG as a v1 contract boundary with schema/query requirements, but defer graph storage and traversal implementation to a later change.
- Establish stable citation, structured error, and explicit empty retrieval behavior.

## Capabilities

### New Capabilities

- `knowledge-provider`: HTTP provider contract for health, catalog, RAG retrieval, and GraphRAG query boundaries.
- `document-rag`: First implementation slice for local document retrieval with compact answer context and stable citations.

### Modified Capabilities

None.

## Impact

- Adds OpenSpec requirements for the provider API and document RAG behavior.
- Adds a Python FastAPI provider scaffold under `app/`.
- Adds focused contract tests for HTTP response shape and retrieval behavior.
- Does not require MyPrivateAgent integration in this change.
- Does not add Neo4j, LlamaIndex, or production vector-store dependencies in the first implementation slice.
