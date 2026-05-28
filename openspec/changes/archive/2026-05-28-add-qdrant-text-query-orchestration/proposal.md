# Proposal: Add Qdrant Text Query Orchestration

## Summary

Connect the existing embedding adapter boundary to Qdrant vector query helpers so Qdrant can execute opt-in text retrieval through `query -> embedding -> vector search -> EvidenceDocument`.

## Motivation

The provider now has:

- Qdrant point/payload/filter mapping
- live Qdrant collection/upsert/vector-query helpers
- a provider-neutral embedding adapter interface

The next safe slice is to orchestrate these pieces for Qdrant text retrieval while keeping production model selection and default backend behavior unchanged.

## Scope

In scope:

- Qdrant text query orchestration helper
- embedding readiness + Qdrant collection readiness composition
- Qdrant document retriever integration for explicit `RAG_RETRIEVAL_BACKEND=qdrant`
- tests using fake clients/adapters
- README and spec documentation updates

Out of scope:

- selecting a production embedding model
- calling hosted embedding APIs
- loading local embedding models
- automatic ingestion from source documents
- reranking
- making Qdrant the default backend
- requiring a live Qdrant service in tests

## Impact

This makes Qdrant a runnable opt-in backend path when a caller supplies a usable Qdrant endpoint and embedding provider. Default fixture and LlamaIndex behavior remain unchanged.
