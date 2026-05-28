# Change: add-bge-m3-local-embedding-adapter

## Summary

Add an opt-in local BGE-M3 embedding adapter for Chinese-heavy RAG evaluation.

## Motivation

Hosted embedding APIs introduce recurring cost and data-egress concerns. The project needs a private-network capable embedding path before production evaluation. BGE-M3 is a strong first local candidate because it is multilingual, supports Chinese-heavy retrieval, outputs 1024-dimensional dense vectors, and leaves room for later sparse/hybrid retrieval work.

This change implements only the dense local adapter path. It keeps the default mock adapter, avoids automatic production promotion, and adds download/offline configuration for China-friendly local setup.

## Goals

- Add `EMBEDDING_PROVIDER=bge_m3_local` as an explicit opt-in adapter.
- Load BGE-M3 through `FlagEmbedding` only when the adapter is selected.
- Return dense 1024-dimensional vectors compatible with the current Qdrant defaults.
- Support local model paths and optional Hugging Face endpoint override for mirror acceleration.
- Keep readiness fail-closed when dependencies or model files are unavailable.

## Non-Goals

- Do not enable BGE-M3 by default.
- Do not implement sparse vectors, ColBERT multi-vector retrieval, reranking, or hybrid search.
- Do not download models during tests.
- Do not hard-code a third-party mirror as the default endpoint.
