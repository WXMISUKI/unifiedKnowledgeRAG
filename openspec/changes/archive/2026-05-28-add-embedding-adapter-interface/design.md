# Design: Embedding Adapter Interface

## Overview

Embedding adapters convert text into vectors. This change adds the contract and a mock implementation only. Real hosted/local adapters remain explicit future work.

## Adapter Contract

`EmbeddingAdapter` exposes:

- `provider_name`
- `model_name`
- `vector_size`
- `embed_text(text)`
- `embed_batch(texts)`
- `readiness()`

The contract returns dense vectors as `list[float]`.

## Mock Adapter

The mock adapter is deterministic and dependency-free:

- it hashes input text into a fixed-size vector
- it normalizes non-empty vectors
- it returns zero vector for empty text

This is not a semantic embedding model. It is a contract-test adapter for wiring Qdrant ingestion/retrieval.

## Hosted and Local Placeholders

Hosted and local provider modes are declared but fail closed:

- `hosted` returns degraded readiness and raises `NotImplementedError`
- `local` returns degraded readiness and raises `NotImplementedError`

This prevents accidental production use before model/provider decisions.

## Configuration

Settings gain:

- `embedding_provider`
- `embedding_model`
- `embedding_vector_size`

Defaults:

- provider: `mock`
- model: `mock-hash-v1`
- vector size: same as Qdrant vector size unless explicitly overridden

## Qdrant Integration Boundary

Helpers can embed `VectorEvidenceChunk` text before upsert, but live Qdrant retrieval still requires future text-query orchestration. This change should not make Qdrant the default backend.
