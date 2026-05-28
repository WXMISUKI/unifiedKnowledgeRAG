# Change: evaluate-chinese-embedding-candidates

## Summary

Add a local embedding candidate evaluation layer for Chinese-heavy RAG workloads. The change records candidate metadata, enterprise decision criteria, and a deterministic evaluation report shape without selecting or calling a real embedding provider yet.

## Motivation

The project now has Qdrant ingestion and text-query orchestration, but the embedding model is still intentionally undecided. Because the target workload is expected to be mostly Chinese and eventually enterprise-scale, model selection should be evidence-driven instead of hard-coded into the provider path.

This change creates a safe next step: compare candidate profiles and readiness assumptions using local metadata and benchmark output contracts, while keeping the default mock embedding and fail-closed real providers.

## Goals

- Define named Chinese embedding candidates with stable ids and metadata for later architecture review.
- Capture enterprise evaluation criteria such as Chinese coverage, deployment mode, data residency, vector dimension, cost, latency, and reranker compatibility.
- Export embedding candidate evaluation evidence as local JSON and Markdown files.
- Keep all real hosted/local embedding providers fail-closed until a later approved implementation change.

## Non-Goals

- Do not implement calls to OpenAI, Qwen, BGE, Jina, or any other hosted/local embedding runtime.
- Do not select a production embedding model.
- Do not change the default retrieval backend or default embedding provider.
- Do not add new public HTTP APIs for benchmark execution.
