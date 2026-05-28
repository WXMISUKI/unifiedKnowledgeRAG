## Why

The first provider slice proves the HTTP contract, but its in-memory lexical retriever is only a fixture. The next step is to introduce a configurable document RAG implementation boundary that can use LlamaIndex for ingestion, node parsing, indexing, retrieval, and citation-preserving evidence assembly.

This change moves document RAG toward production architecture while preserving the v1 provider API that MyPrivateAgent will call.

## What Changes

- Introduce a configurable document RAG backend abstraction.
- Add a LlamaIndex-backed implementation path for local document indexing and retrieval.
- Preserve existing `/api/rag/retrieve` request and response contracts.
- Add source-level backend metadata so catalog readiness distinguishes fixture, local index, and future production vector-store modes.
- Add environment-driven configuration for index storage, source document paths, embedding mode, and retrieval backend.
- Keep GraphRAG behavior unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `document-rag`: Document retrieval requirements now include backend selection, LlamaIndex local indexing, citation preservation, and fallback behavior.
- `knowledge-provider`: Catalog and health requirements now include backend readiness metadata for document RAG.

## Impact

- Adds LlamaIndex as a planned document RAG dependency in the `GRAPHRAG` conda environment and project dependency files.
- Adds configuration and service boundaries under `app/`.
- Replaces direct lexical retrieval coupling with an interface that supports `fixture` and `llamaindex` backends.
- Adds tests for backend selection, citation stability, and readiness behavior.
- Does not change GraphRAG query implementation.
