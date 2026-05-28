# Proposal: Add Qdrant Source Ingestion Flow

## Summary

Add an explicit Qdrant source ingestion flow that reads configured local source documents, creates evidence chunks, embeds them through the configured embedding adapter, upserts them to Qdrant, and marks the source index ready.

## Motivation

The provider can now execute Qdrant text queries, but Qdrant still lacks a source ingestion path connected to the existing ingestion lifecycle. Without that, `RAG_RETRIEVAL_BACKEND=qdrant` can query Qdrant only if data was inserted manually.

This change connects the existing local source documents to the Qdrant adapter while preserving the current guardrails:

- Qdrant remains explicit opt-in.
- Mock embedding remains contract-only.
- Real hosted/local embedding candidates remain future decisions.
- Tests do not require an external Qdrant service.

## Scope

In scope:

- markdown source loading for Qdrant ingestion
- deterministic structure-aware-ish chunk creation for local source docs
- chunk metadata preservation for tenant/source/document/citation
- embedding chunks through the configured embedding adapter
- Qdrant upsert through the existing adapter helper
- integration with `create_ingestion_job` / queued ingestion lifecycle
- tests with fake Qdrant client
- README/spec documentation updates

Out of scope:

- production document parser selection
- PDF/Word/table parsing
- chunking strategy finalization for enterprise corpora
- real hosted/local embedding model selection
- reranker
- GraphRAG
- background worker infrastructure

## Impact

Qdrant can now participate in the same ingestion lifecycle as LlamaIndex when explicitly selected. The default fixture backend and existing LlamaIndex behavior remain unchanged.
