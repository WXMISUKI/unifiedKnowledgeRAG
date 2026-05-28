# Design: Qdrant Source Ingestion Flow

## Overview

The ingestion flow composes existing building blocks:

1. Resolve source markdown path from `RAG_SOURCE_DIR`.
2. Convert source content to one or more `VectorEvidenceChunk` items.
3. Embed chunks with `EmbeddingAdapter`.
4. Ensure Qdrant collection exists.
5. Upsert chunks.
6. Write source index status to the lifecycle store.

## Chunking

This slice uses a simple markdown-aware paragraph chunker:

- heading becomes title context
- non-empty paragraphs become chunks
- each chunk gets a stable `chunk_id`
- citation defaults to `<document_id>#chunk-<n>`

This is deliberately not the final enterprise chunking strategy. Future changes should evaluate structure-aware and token-aware chunking with benchmark evidence.

## Metadata

Each Qdrant chunk payload includes:

- `tenant_id`
- `source_id`
- `document_id`
- `chunk_id`
- `title`
- `text`
- `citation`
- `embedding_provider`
- `embedding_model`
- `chunking_strategy`

## Lifecycle Integration

`index_lifecycle._build_source_index(...)` gains a Qdrant branch. When the backend is `qdrant`, ingestion builds and upserts Qdrant chunks, then writes `IndexStatusResponse(status="ready", backend="qdrant")`.

## Test Strategy

Tests monkeypatch Qdrant client creation with fake clients. No Docker Qdrant is required for automated tests.
