## Context

`add-llamaindex-document-rag` introduced a configurable document RAG backend and a local LlamaIndex path using `MockEmbedding`. That slice intentionally kept indexing simple: readiness and retrieval both call into local index construction. This is useful for contract validation, but it hides an important production boundary. Indexing is a lifecycle operation with its own state, failures, retries, and observability; retrieval should not be the first place callers discover that a source has not been indexed.

The provider is still the knowledge data plane for MyPrivateAgent. MyPrivateAgent should be able to ask for source status, start indexing, and retrieve evidence through provider-neutral contracts without owning vector store internals.

## Goals / Non-Goals

**Goals:**

- Add explicit local ingestion job and source index status contracts.
- Separate backend process readiness from per-source index lifecycle readiness.
- Keep first implementation deterministic and in-process so it remains easy to test in the `GRAPHRAG` environment.
- Preserve `/api/rag/retrieve` response shape while making unindexed sources fail with structured provider errors.
- Prepare a clean seam for future queue-backed indexing, persistent job stores, vector databases, rerankers, and incremental indexing.

**Non-Goals:**

- No external queue, worker service, database migration, or distributed scheduler.
- No production vector store migration.
- No document upload, document parser pipeline, chunking strategy overhaul, or reranker.
- No auth/tenant policy. Those controls belong in a later provider governance slice.

## Decisions

1. Introduce a small index lifecycle service rather than putting job state inside the router.

   The service owns job creation, status transitions, source validation, and local build orchestration. Routers only translate HTTP requests/responses. This keeps future queue-backed execution behind a stable service boundary.

2. Model index lifecycle separately from backend readiness.

   Backend readiness answers "can this backend operate"; index lifecycle answers "has this source been indexed and when". Health/catalog should include both so degraded source state does not masquerade as a provider outage.

3. Use in-memory job records for the first slice.

   The current project has no persistence layer. In-memory records are sufficient for local contract tests and keep the slice focused. The API contract should avoid promising durability until a later change introduces a persistent job store.

4. Make local jobs synchronous internally while returning a job envelope.

   `POST /api/ingestion/jobs` may complete the local build before returning, but the response is still a job resource with status and timestamps. This preserves a future async migration path without requiring background infrastructure now.

5. Refactor LlamaIndex build orchestration behind explicit methods.

   `LlamaIndexLocalRetriever` should expose reusable build/load helpers or delegate to a dedicated index manager. Retrieval should check lifecycle status before querying so callers get deterministic `INDEX_NOT_READY` errors instead of hidden startup work.

## Risks / Trade-offs

- In-memory job state disappears on process restart -> document the local-only behavior and expose source-level status derived from filesystem/index state where possible.
- Synchronous local jobs can block a request for large sources -> keep fixture documents tiny and mark production queueing as a future change.
- Source status can become inconsistent if files are manually changed -> include freshness/index timestamp fields and keep incremental indexing out of scope for this slice.
- Introducing lifecycle state may change health semantics -> preserve provider health shape and add fields rather than replacing existing readiness fields.

## Migration Plan

1. Add lifecycle models and service with fixture-backed local job store.
2. Add routers for job creation and index status.
3. Wire routes into `create_app()`.
4. Refactor the LlamaIndex backend to support explicit build/status checks.
5. Update health/catalog/readiness metadata to include source index lifecycle.
6. Add focused tests and README documentation.
7. Validate with `conda run -n GRAPHRAG python -m pytest -q` and `openspec validate add-explicit-index-lifecycle --strict`.
