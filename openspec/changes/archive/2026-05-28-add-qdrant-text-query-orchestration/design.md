# Design: Qdrant Text Query Orchestration

## Overview

Qdrant text query orchestration composes existing adapter layers:

1. Validate requested knowledge base ids.
2. Embed the query text through `EmbeddingAdapter`.
3. Query Qdrant with the resulting vector and payload filters.
4. Map valid hits to `EvidenceDocument`.

## Helper Boundary

Add `query_qdrant_documents_for_text(...)` to the Qdrant adapter module. It accepts injected client and embedding adapter objects, which keeps tests deterministic and avoids requiring live Qdrant.

## Retriever Integration

`QdrantDocumentRetriever` can use the orchestration helper when Qdrant is explicitly selected. It remains opt-in through `RAG_RETRIEVAL_BACKEND=qdrant`.

## Readiness

Readiness combines:

- embedding adapter readiness
- Qdrant collection readiness

If either is degraded, Qdrant readiness is degraded with a combined reason.

## Guardrails

- Default retrieval backend remains `fixture`.
- Mock embedding remains deterministic wiring only, not semantic quality.
- Hosted/local embedding providers still fail closed until implemented.
- Tests use fake clients and fake hits.
