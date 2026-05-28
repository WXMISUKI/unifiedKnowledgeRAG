# Proposal: Add Live Qdrant Ingestion Retrieval

## Summary

Add a live Qdrant client adapter for collection readiness, chunk upsert, and vector query result mapping while keeping Qdrant opt-in and embedding generation undecided.

## Motivation

The previous Qdrant slice established configuration, point payload mapping, and candidate metadata. The next step is to make Qdrant executable enough for local/public-network tests and future private-network deployment:

- create or verify a Qdrant collection
- upsert evidence chunks that already have vectors
- query by an externally supplied vector
- map Qdrant hits back to provider `EvidenceDocument` results

This keeps the vector database path concrete without prematurely selecting a production embedding model or reranker.

## Scope

In scope:

- `qdrant-client` runtime dependency
- lazy Qdrant client construction
- collection creation/readiness helper
- chunk upsert helper
- vector query helper with source/tenant filters
- Qdrant hit to `EvidenceDocument` mapping
- focused tests using fake clients
- README and architecture documentation updates

Out of scope:

- embedding model selection
- query text embedding generation
- reranker implementation
- background ingestion worker
- making Qdrant the default backend
- requiring Docker Qdrant during automated tests
- GraphRAG / Neo4j implementation

## Impact

The default retrieval backend remains `fixture`. Qdrant remains explicit opt-in. The live adapter can be used by later ingestion and retrieval changes once an embedding adapter is selected.
