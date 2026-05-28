# Proposal: Add Embedding Adapter Interface

## Summary

Add a provider-neutral embedding adapter interface with a deterministic mock implementation and explicit hosted/local configuration boundaries.

## Motivation

The Qdrant live adapter now accepts vectors but intentionally does not choose or call an embedding model. The next safe slice is to define the embedding boundary so future hosted and private-network embedding candidates can plug into Qdrant without changing retrieval contracts.

This keeps the project aligned with the public-network/local-test and private-network/enterprise deployment split:

- public-network testing can use hosted embedding adapters later
- private-network deployment can use local Chinese/bilingual embedding adapters later
- current tests remain deterministic with a mock embedding adapter

## Scope

In scope:

- embedding provider settings
- embedding adapter abstract interface
- deterministic mock embedding adapter
- explicit hosted/local placeholder adapters that fail closed until implemented
- helper to embed query text and evidence chunks
- tests for deterministic vectors, vector size, and fail-closed placeholders
- README and architecture documentation updates

Out of scope:

- selecting BGE-M3, Qwen, OpenAI, Jina, or any production embedding model
- calling external embedding APIs
- loading local embedding model weights
- reranker implementation
- switching default retrieval backend to Qdrant
- end-to-end text query retrieval through Qdrant

## Impact

This change introduces the embedding boundary needed by later Qdrant retrieval and ingestion changes. The default embedding provider is deterministic `mock`, suitable only for contract tests and local adapter plumbing.
