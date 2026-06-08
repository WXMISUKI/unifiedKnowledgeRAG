## Why

The provider has completed the local company-profile PDF/parser-derived RAG trial with grounded answers and negative controls, but those trial questions are not yet reusable as a stable quality baseline. Before adopting advanced RAG techniques from `RAG_Techniques`, the project needs repeatable golden cases and chunk-quality diagnostics that classify real failures instead of promoting query rewrite, rerank, hybrid retrieval, RAPTOR, or GraphRAG by popularity.

## What Changes

- Add a provider-local golden-case baseline for the approved company-profile business corpus.
- Add chunk-quality diagnostics for the same corpus, including chunk count, tiny/noisy chunk signals, citation coverage, page/section provenance coverage, and retrieval outcomes.
- Add a read-only exporter that writes JSON and Markdown reports under `docs/local-run/business-rag-golden-cases/`.
- Reuse existing retrieve/answer/evidence-pack behavior and preserve fail-closed insufficient-evidence expectations.
- Keep runtime defaults unchanged.

## Capabilities

### New Capabilities
- `local-business-rag-golden-cases`: Defines reusable local business RAG golden cases and chunk-quality baseline evidence for approved local business corpora.

### Modified Capabilities
- `provider-roadmap`: Records that this RAG_Techniques-inspired next stage is closed by golden-case and chunk-quality baseline evidence rather than advanced runtime RAG promotion.

## Impact

- Adds a local fixture or generated case source for `company_profile_2025_trial`.
- Adds a lightweight exporter script for local evidence generation.
- Adds focused tests for `go`, `review`, and `blocked` report decisions.
- Updates roadmap/progress documentation after implementation.
- No public HTTP API changes.
- No parser engine adoption, source binding, MyPrivateAgent orchestration, vector backend promotion, reranker, hybrid retrieval, GraphRAG, or runtime default change.
