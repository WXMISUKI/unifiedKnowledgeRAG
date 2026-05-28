## Context

The repository currently contains design documents for an external RAG / GraphRAG provider, but no OpenSpec baseline and no runtime implementation. The target architecture separates MyPrivateAgent as the runtime control plane from unifiedKnowledgeRAG as the knowledge data plane.

The provider must eventually manage document ingestion, chunking, embeddings, vector retrieval, graph schemas, graph traversal, ontology versions, evidence, and index lifecycle. The first implementation must stay small enough to verify: document RAG only, backed by static local catalog data and a lightweight deterministic retriever.

## Goals / Non-Goals

**Goals:**

- Define one provider contract that includes RAG and GraphRAG boundaries.
- Implement a minimal document RAG provider slice with stable HTTP JSON contracts.
- Return machine-readable readiness from health, capabilities, catalog, and source endpoints.
- Return compact retrieval context, stable citations, explicit empty results, and structured errors.
- Keep the service independently runnable and testable without MyPrivateAgent.

**Non-Goals:**

- No MyPrivateAgent `/api/chat` automatic injection.
- No provider-side document upload or index mutation APIs.
- No Neo4j graph implementation in this first slice.
- No production LlamaIndex integration in this first slice.
- No OCR, reranking, incremental indexing, or tenant isolation implementation yet.

## Decisions

### Decision 1: Provider-first HTTP boundary

The provider exposes FastAPI endpoints and provider-neutral Pydantic models. MyPrivateAgent will consume capability IDs and source IDs, not Python classes or framework objects.

Alternatives considered:

- Import provider internals into MyPrivateAgent: rejected because it couples the control plane to retrieval frameworks.
- Build one service per vertical agent: rejected for v1 because source catalog and lifecycle operations are easier to govern centrally.

### Decision 2: Contract includes GraphRAG, implementation starts with document RAG

The OpenSpec contract defines graph schema/query expectations now, while the first provider runtime returns graph capability metadata but does not implement graph query execution.

Alternatives considered:

- Exclude graph entirely from v1 specs: rejected because MyPrivateAgent source binding needs stable future names and boundaries.
- Implement graph in the first slice: rejected because graph storage, ontology, traversal, and evidence normalization are separate risks.

### Decision 3: Deterministic local retriever before LlamaIndex

The first implementation uses a small local JSON catalog and deterministic lexical scoring to prove API shape and citations. The service boundary is named so the implementation can later be replaced by LlamaIndex/vector retrieval without changing HTTP callers.

Alternatives considered:

- Add LlamaIndex immediately: rejected for first slice because dependency and index setup would obscure contract validation.
- Return mock static payloads only: rejected because smoke tests should exercise real filtering and empty retrieval behavior.

### Decision 4: Structured success and failure envelope

All provider operations return explicit success or structured error envelopes. Empty retrieval is a successful result with empty documents and empty answer context.

Alternatives considered:

- Use raw FastAPI validation errors as the only error model: rejected because MyPrivateAgent needs stable provider error codes.
- Return free-text degraded states: rejected because readiness must be machine-readable.

## Risks / Trade-offs

- Lightweight lexical retrieval may be mistaken for production RAG -> Keep class names and docs clear that this is a first-slice retriever.
- Graph endpoints without execution may look incomplete -> Expose graph schema metadata and return `GRAPH_NOT_IMPLEMENTED` for query until the graph change lands.
- Static catalog can drift from real sources -> Keep catalog data centralized in one service module and covered by tests.
- Contract may evolve after MyPrivateAgent integration -> Keep v1 small and archive only after smoke validation.

## Migration Plan

1. Add OpenSpec change artifacts and validate them.
2. Add provider package, routes, contracts, services, and tests.
3. Verify with pytest and a local FastAPI TestClient smoke path.
4. Later changes may replace lexical retrieval with LlamaIndex-backed indexing behind the same service interface.

Rollback is simple for v1: remove the provider package and OpenSpec change before archive if contract validation fails.

## Open Questions

- Which embedding provider and vector store should become the production default after the contract slice is accepted?
- Should graph query return HTTP 501 while the capability is advertised as planned, or should graph capability be hidden until implemented?
- Which source catalog storage should replace static local data: YAML, database table, or operator-managed API?
