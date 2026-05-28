# Design: Qdrant Vector Store Candidate Adapter

## Overview

The adapter introduces a provider-neutral vector point model and a Qdrant-specific mapper. This keeps Qdrant details away from the HTTP contract and gives us a stable place to test enterprise metadata fields before live indexing.

## Qdrant Fit

Qdrant organizes data into collections of points. Points can carry vectors and payload metadata. Its payload indexes and filtering model align with the enterprise RAG needs we have identified: tenant isolation, source filtering, document versioning, and access-control tags.

## Data Model

`VectorEvidenceChunk` contains:

- `point_id`
- `source_id`
- `document_id`
- `chunk_id`
- `title`
- `text`
- `citation`
- `vector`
- `metadata`

Required payload fields:

- `tenant_id`
- `source_id`
- `document_id`
- `chunk_id`
- `citation`
- `title`

Optional payload fields may include:

- `document_version`
- `acl_tags`
- `embedding_model`
- `chunking_strategy`
- `created_at`
- `updated_at`

## Adapter Behavior

The Qdrant adapter maps provider-neutral chunks into Qdrant-style point structures:

- point id remains stable
- vector is stored under a named vector key
- payload keeps source, tenant, citation, and optional metadata

It also builds filter metadata for source-level and tenant-level retrieval. This first slice does not execute live Qdrant calls in tests.

## Configuration

Settings gain Qdrant candidate fields:

- `qdrant_url`
- `qdrant_api_key`
- `qdrant_collection`
- `qdrant_vector_name`
- `qdrant_vector_size`

The API key remains optional so local Docker and future private-network deployments can work without hard-coding secrets.

## Guardrails

- Qdrant is not the default backend.
- No production embedding model is selected.
- The adapter is tested through deterministic mapping and metadata validation.
- Live Qdrant connectivity can be added later behind explicit readiness checks.
