## Context

`add-knowledge-provider-v1` established a provider contract and a deterministic fixture retriever. That implementation is useful for contract testing, but it does not model real document ingestion, chunking, index persistence, or retrieval behavior.

The provider should now evolve toward the originally documented architecture: LlamaIndex is used inside the provider, while MyPrivateAgent continues to call stable HTTP endpoints and receives provider-neutral evidence documents.

## Goals / Non-Goals

**Goals:**

- Add a backend abstraction for document retrieval.
- Support a `fixture` backend for fast deterministic tests.
- Support a `llamaindex` backend for local document indexing and retrieval.
- Keep `/api/rag/retrieve` response shape unchanged.
- Preserve stable citations using provider-owned metadata.
- Report backend readiness through health and catalog metadata.
- Make all Python commands run under the `GRAPHRAG` conda environment.

**Non-Goals:**

- No MyPrivateAgent integration change.
- No remote vector database in this change.
- No OCR, reranker, incremental job queue, or lifecycle mutation endpoints.
- No GraphRAG implementation change.
- No automatic LLM answer generation; this provider returns evidence context only.

## Decisions

### Decision 1: Backend interface before LlamaIndex wiring

Define a provider-owned retriever interface with `retrieve(request) -> RagRetrieveResponse`. The existing fixture retriever remains available for deterministic tests, and LlamaIndex becomes a second backend selected through configuration.

Alternatives considered:

- Replace the fixture directly: rejected because contract tests need stable, fast behavior.
- Let routes import LlamaIndex directly: rejected because routers should stay HTTP-focused and framework-neutral.

### Decision 2: Use local persisted index for the first LlamaIndex slice

The first LlamaIndex implementation builds or loads a local persisted index from configured source documents. This avoids requiring a production vector store before the provider contract is integrated.

Alternatives considered:

- Use Qdrant immediately: rejected because vector-store operations and deployment are a separate concern.
- Rebuild index on every request: rejected because health/readiness and retrieval latency would be unstable.

### Decision 3: Use explicit citation metadata

Every node indexed by LlamaIndex must carry provider-owned metadata: `source_id`, `document_id`, `title`, and `citation`. Retrieval responses are assembled from this metadata instead of leaking framework objects.

Alternatives considered:

- Generate citations from file paths at response time: rejected because citations would change when storage layout changes.
- Return LlamaIndex source node payloads directly: rejected because provider contracts must stay JSON stable and framework-neutral.

### Decision 4: Health reports configured backend status

Health and catalog metadata include backend name, index path, and readiness status. If the `llamaindex` backend is configured but the index cannot load or build, health returns degraded instead of hiding the problem behind empty retrieval.

Alternatives considered:

- Keep health independent of backend: rejected because MyPrivateAgent needs heartbeat visibility.
- Fail process startup when index is unavailable: rejected for local development, where degraded health is easier to diagnose.

## Risks / Trade-offs

- LlamaIndex dependency versions can move quickly -> Pin dependencies and verify inside `GRAPHRAG`.
- Local embeddings may not represent production quality -> Treat the first slice as architecture enablement, not final retrieval quality.
- Index rebuild may be slow for larger corpora -> Keep v2 local documents small and defer ingestion jobs.
- Citation metadata can be missing in source fixtures -> Validate source records before indexing and fail readiness clearly.

## Migration Plan

1. Add dependency file and install dependencies in `GRAPHRAG`.
2. Add configuration model for backend and paths.
3. Extract fixture retrieval behind a backend interface.
4. Add LlamaIndex backend that loads/builds local persisted index.
5. Preserve current contract tests and add backend-specific tests.
6. Update README with `conda run -n GRAPHRAG` commands.

Rollback: set `RAG_RETRIEVAL_BACKEND=fixture` and keep existing deterministic retriever behavior.

## Open Questions

- Which embedding mode should be default for offline local development: LlamaIndex mock embeddings or a local HuggingFace embedding model?
- Should index build be explicit through a CLI command in this change, or lazy on provider startup?
- Should source documents be represented as YAML catalog records plus markdown files, or one JSON manifest for v2?
