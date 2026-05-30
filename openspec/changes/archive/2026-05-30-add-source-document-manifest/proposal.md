## Why

The provider roadmap says Phase 2 should make enterprise document ingestion diagnosable before heavier retrieval or GraphRAG promotion. Callers can list RAG sources today, but they cannot inspect which source documents, citation anchors, or chunking assumptions sit behind a source without running retrieval.

## What Changes

- Add a read-only source document manifest endpoint for a single RAG source.
- Expose stable document ids, source paths, formats, versions, citation anchors, chunking strategy metadata, and current index readiness metadata.
- Return structured provider errors for unknown sources.
- Keep the manifest diagnostic-only: it must not run retrieval, embedding, indexing, Qdrant queries, or graph execution.

## Capabilities

### New Capabilities

### Modified Capabilities

- `document-rag`: add a Phase 2 source document manifest requirement for document diagnostics.

## Impact

- Adds one lightweight HTTP API under `/api/rag/sources/{source_id}/documents`.
- Extends provider contract models with source document manifest response types.
- Adds tests and README guidance for caller integration and diagnostics.
- No new runtime dependency, vector-store dependency, embedding model change, or GraphRAG behavior change.
