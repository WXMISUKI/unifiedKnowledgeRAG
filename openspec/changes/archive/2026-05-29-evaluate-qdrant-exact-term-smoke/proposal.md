# Change: evaluate-qdrant-exact-term-smoke

## Why

The project now has a dedicated exact-term and identifier-heavy benchmark fixture covering policy codes, form names, workflow acronyms, and order-like ids. Before adding sparse vectors, BM25, dense+sparse hybrid search, or reranking, we need local evidence showing how the current Qdrant + BGE-M3 dense-only candidate behaves on those cases.

## What Changes

- Align Qdrant local markdown citation anchors with the exact-term source paragraphs.
- Add a named exact-term Qdrant+BGE smoke evidence export path.
- Export durable local JSON and Markdown evidence for the exact-term fixture.
- Document whether dense-only retrieval is sufficient for this seed or whether hybrid retrieval needs a follow-up evidence slice.

## Non-Goals

- Do not promote Qdrant as the default retrieval backend.
- Do not add sparse vectors, BM25, hybrid query fusion, reranking, or GraphRAG storage.
- Do not change public HTTP contracts.
- Do not treat this seed evidence as production acceptance.

## Validation

- `cmd /c openspec validate evaluate-qdrant-exact-term-smoke --strict`
- Focused pytest for Qdrant citation mapping and benchmark export.
- Full pytest suite.
- Local Qdrant+BGE exact-term evidence export.
