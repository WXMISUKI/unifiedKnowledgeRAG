## Context

`unifiedKnowledgeRAG` is a lightweight external knowledge provider. The roadmap keeps document ingestion, retrieval quality, evidence packaging, and GraphRAG as separate gates. The current source catalog exposes high-level source readiness, while retrieval and answer endpoints expose evidence only after a query. Phase 2 needs a small diagnostic surface that shows how configured sources map to source documents and stable citations without adding production infrastructure.

## Goals / Non-Goals

**Goals:**

- Provide a caller-friendly manifest for one RAG source's backing documents.
- Include enough metadata for MyPrivateAgent or operators to diagnose citation coverage, local source paths, index readiness, and chunking assumptions.
- Keep the endpoint read-only and cheap enough for control-plane preflight or troubleshooting.

**Non-Goals:**

- Do not trigger document parsing, retrieval, embedding, vector queries, ingestion jobs, or graph traversal.
- Do not choose or promote Qdrant, BGE-M3, hybrid retrieval, reranking, or GraphRAG defaults.
- Do not move caller-owned agent policy, source binding decisions, or final answer composition into this provider.

## Decisions

- Add `GET /api/rag/sources/{source_id}/documents` instead of expanding retrieval responses. Retrieval remains focused on query-time evidence; the manifest is source-time diagnostics.
- Use static provider-owned manifests for the existing local markdown sources. This matches the current fixture corpus and avoids hidden filesystem scanning or runtime parsing.
- Include index lifecycle metadata from the existing index status service. This gives useful readiness context while avoiding backend retriever construction.
- Return the existing `ProviderError` envelope for unknown sources. This keeps error handling aligned with retrieval and answer contracts.

## Risks / Trade-offs

- Static manifests can drift from source files if documents are edited without updating metadata. Mitigation: tests assert core local fixtures and README documents the endpoint as provider-owned metadata.
- Citation anchors are source-level diagnostics, not proof that every chunking candidate emits exactly the same chunks. Mitigation: expose `chunking_strategy` and keep chunking promotion under separate benchmark-backed changes.
- The endpoint exposes local source paths. Mitigation: paths are repo-relative provider paths for diagnostics, not absolute host paths or credentials.
