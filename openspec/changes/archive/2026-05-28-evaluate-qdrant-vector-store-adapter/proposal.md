# Proposal: Evaluate Qdrant Vector Store Adapter

## Summary

Add a local Qdrant vector-store candidate adapter surface so we can evaluate Qdrant as the first production vector database candidate without locking in a production embedding model or requiring a running Qdrant service for normal tests.

## Motivation

The project needs a vector database path that works for both:

- public-network local experimentation on the developer machine
- future private-network enterprise deployment

The current recommendation is to evaluate Qdrant first because it is a dedicated vector database with payload filtering, named vector support, and hybrid retrieval capability. We need a small, reversible adapter slice that makes Qdrant concrete enough to test metadata mapping and candidate registration while keeping the main provider contract stable.

## Scope

In scope:

- Qdrant configuration fields in settings
- provider-neutral vector point model for indexed evidence chunks
- Qdrant adapter helper that maps evidence chunks to Qdrant point payloads
- source/tenant/document metadata filter construction
- candidate metadata that can be used by the benchmark evaluation harness
- README and architecture documentation updates

Out of scope:

- selecting a production embedding model
- embedding generation service
- live Qdrant Docker orchestration
- switching default retrieval backend to Qdrant
- hybrid sparse retrieval implementation
- reranker implementation
- GraphRAG / Neo4j implementation

## Impact

This is an evaluation slice. The default backend remains `fixture`, and production retrieval behavior does not change. Future changes can add live Qdrant ingestion and retrieval only after candidate benchmark evidence is available.
