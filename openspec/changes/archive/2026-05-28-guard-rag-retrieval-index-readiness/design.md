## Context

The provider now has explicit ingestion jobs, durable source index status, Qdrant ingestion, and an opt-in local BGE-M3 embedding path. `POST /api/rag/retrieve` still performs backend retrieval before it checks source index readiness, so a production backend can do unnecessary external work before the API returns `INDEX_NOT_READY`.

Qdrant also has a temporary `not_ready_sources` implementation that marks every known source as not ready, regardless of the persisted lifecycle marker written by ingestion. That keeps the contract safe, but it blocks successful retrieval after a Qdrant source has been indexed.

## Goals / Non-Goals

**Goals:**

- Make source id validation and lifecycle readiness checks happen before backend retrieval.
- Preserve the existing HTTP response contract and error codes.
- Use persisted `IndexLifecycleStore` source status as the canonical Qdrant readiness gate.
- Add focused regression coverage that proves not-ready Qdrant sources do not query Qdrant or embed the query.

**Non-Goals:**

- Do not change embedding model selection, vector database choice, or chunking strategy.
- Do not add a background worker, queue service, reranker, or graph traversal.
- Do not alter fixture backend behavior.

## Decisions

1. Keep the route-level gate in `app.routers.rag`.

   The route owns HTTP response shaping, so it is the right place to return `UNKNOWN_KNOWLEDGE_BASE` and `INDEX_NOT_READY` before backend work starts. Backends still keep their own defensive checks because services may be called directly by tests or future internal jobs.

2. Add an explicit `unknown_sources` method to the retriever interface.

   Today source validation is coupled to `retrieve()`. Splitting it lets the route validate inputs before retrieval while keeping backend-specific unknown source behavior available for Qdrant and future providers.

3. Make Qdrant `not_ready_sources` delegate to index lifecycle status.

   Qdrant ingestion already writes `status=ready` for a source after upsert. Retrieval readiness should read that marker instead of using a blanket “known source means not ready” placeholder.

## Risks / Trade-offs

- [Risk] Changing route ordering could expose tests that relied on backend calls for readiness behavior. -> Mitigation: keep backend defensive checks and add API-level regression tests for the new ordering.
- [Risk] Qdrant retrieval can still fail after readiness passes if the external collection was deleted. -> Mitigation: backend readiness still checks collection availability; this change only gates source lifecycle readiness before query execution.
- [Risk] Existing persisted status could be stale. -> Mitigation: this is already the lifecycle contract; future changes can add source checksums or collection payload audits without changing the retrieval gate.
