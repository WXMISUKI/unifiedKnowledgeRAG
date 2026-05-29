# Change: evaluate-qdrant-hybrid-exact-term-candidate

## Why

Qdrant+BGE-M3 dense-only exact-term smoke evidence now misses two of four identifier-heavy cases at `RAG_SCORE_THRESHOLD=0.7`: the form name `AF-REFUND-02` and the order-like id `ORD-ZS-2026-0007`. That is enough evidence to evaluate a sparse or dense+sparse candidate, but not enough to promote hybrid retrieval into runtime defaults.

## What Changes

- Add an evaluation-only Qdrant dense+sparse hybrid smoke path using named dense and sparse vectors.
- Generate deterministic lexical sparse vectors for exact terms, acronyms, form names, and order-like ids without adding a new model dependency.
- Export local JSON and Markdown evidence for the exact-term fixture using stable hybrid candidate filenames.
- Document whether hybrid improves exact-term recall and what gates remain before runtime promotion.

## Non-Goals

- Do not change the default retrieval backend.
- Do not change runtime Qdrant ingestion defaults.
- Do not add a production sparse embedding model, BM25 service, reranker, or GraphRAG storage.
- Do not change public HTTP contracts.
- Do not treat exact-term seed evidence as production acceptance.

## Validation

- `cmd /c openspec validate evaluate-qdrant-hybrid-exact-term-candidate --strict`
- Focused pytest for sparse vector generation, hybrid Qdrant query shape, and exact-term evidence export.
- Full pytest suite.
- Local Qdrant+BGE hybrid exact-term evidence export.
