# Design: Live Qdrant Ingestion Retrieval

## Overview

This change adds a thin Qdrant client adapter around the existing provider-neutral vector chunk model. It should be usable with a local Docker Qdrant instance, Qdrant local mode, or a private-network Qdrant endpoint, but tests should not require any external service.

## Adapter Functions

The adapter exposes:

- `create_qdrant_client(settings)` for lazy client construction
- `ensure_qdrant_collection(client, settings)` for collection readiness
- `upsert_qdrant_chunks(client, chunks, settings)` for batch point writes
- `query_qdrant_documents(client, query_vector, source_ids, settings, ...)` for vector lookup

## Dependency Boundary

`qdrant-client` is added as an explicit dependency, but imports remain localized to the Qdrant adapter. The rest of the provider should continue to run with fixture and LlamaIndex paths.

## Embedding Boundary

The query helper accepts a vector. It does not embed text. This preserves the open embedding decision and allows future hosted/local embedding adapters to share the same vector-store adapter.

## Result Mapping

Qdrant payload hits are mapped into `EvidenceDocument`:

- `source_id`
- `document_id`
- `title`
- `snippet` from payload `text`
- score from the Qdrant hit
- `citation`

Missing required payload fields are skipped instead of producing partial evidence documents.

## Readiness

Collection readiness is checked through the Qdrant client and returns `(status, reason)`:

- `ready` when the collection exists or is created
- `degraded` when Qdrant is unreachable or the collection cannot be prepared

## Guardrails

- No live Qdrant calls are made during default app startup unless Qdrant is explicitly selected.
- Tests use fake clients.
- Qdrant retrieval backend still reports degraded for text queries until embedding is selected.
- Query text embedding and reranking are separate future changes.
