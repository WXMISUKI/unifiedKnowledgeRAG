# Change: evaluate-qdrant-hybrid-empty-stress

## Why

The evaluation-only Qdrant dense+sparse hybrid candidate recovered all exact-term identifier cases, but that fixture contains no expected-empty cases. Sparse token overlap can improve exact-term recall while also increasing false positives for unsupported questions that share policy codes, form names, workflow acronyms, or order-like ids.

Before discussing runtime hybrid promotion, the provider needs local evidence for hybrid empty-query behavior.

## What Changes

- Add a dedicated hybrid empty-stress benchmark fixture with unsupported but token-overlapping enterprise questions.
- Add a named Qdrant+BGE hybrid empty-stress evidence export path.
- Export local JSON and Markdown evidence showing whether hybrid returns unexpected evidence.
- Document the promotion boundary after the empty-stress result.

## Non-Goals

- Do not change runtime retrieval defaults.
- Do not change public HTTP contracts.
- Do not replace the main Chinese seed or exact-term fixture.
- Do not add a production sparse embedding model, BM25 service, reranker, or GraphRAG storage.
- Do not approve hybrid retrieval for production.

## Validation

- `cmd /c openspec validate evaluate-qdrant-hybrid-empty-stress --strict`
- Focused pytest for fixture loading and hybrid empty-stress export shape.
- Full pytest suite.
- Local Qdrant+BGE hybrid empty-stress evidence export.
