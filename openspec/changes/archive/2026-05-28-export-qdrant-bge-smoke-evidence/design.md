## Context

Qdrant ingestion writes source status through the lifecycle store and Qdrant retrieval can query text through the configured embedding adapter. The benchmark harness already exports JSON and Markdown evidence for retrieval candidates. What is missing is a narrow helper that assembles these pieces for an end-to-end local smoke run.

The smoke path should be able to use real BGE-M3 locally, but tests must not load the model. Therefore the implementation should accept normal `Settings` and rely on the embedding adapter boundary, while tests use mocked adapters/clients.

## Goals / Non-Goals

**Goals:**

- Index selected local sources into a single Qdrant client.
- Query selected benchmark cases against the same Qdrant client.
- Export JSON and Markdown evidence with metrics and environment metadata.
- Support real BGE-M3 by configuration without making it the default.
- Keep the implementation service-level and script-driven.

**Non-Goals:**

- Do not promote Qdrant or BGE-M3 as production defaults.
- Do not add reranking, hybrid retrieval, sparse vectors, or graph traversal.
- Do not add HTTP endpoints or background worker behavior.
- Do not replace the existing benchmark candidate exports.

## Decisions

1. Use a single Qdrant client for the entire smoke run.

   This avoids `:memory:` isolation issues and mirrors the logical shape of a local Qdrant instance: ingest first, query second, export results third.

2. Build a smoke-specific report instead of overloading candidate evaluation.

   Candidate evaluation assumes backend selection through `create_document_retriever`, which creates its own Qdrant client. The smoke helper needs a shared client, source indexing metadata, and environment metadata, so a dedicated report type is clearer and safer.

3. Keep expected metrics compatible with the existing benchmark report shape.

   The helper should reuse `RetrievalBenchmarkCaseResult`, `_summarize`, and the Markdown table style so later evidence comparison remains familiar.

## Risks / Trade-offs

- [Risk] Real BGE-M3 smoke can be slow on CPU. -> Mitigation: the script is opt-in, supports limiting cases and sources, and tests mock the heavy adapter.
- [Risk] In-memory Qdrant evidence is not proof of production persistence. -> Mitigation: report metadata records `qdrant_url` and the README labels it as smoke evidence, not production acceptance.
- [Risk] Seed benchmark cases may expect citations from fixture sections while Qdrant chunking emits chunk citations. -> Mitigation: smoke evidence records actual citations and metrics; misses become useful evidence for later chunking/reranker work.
