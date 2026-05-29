# expand-exact-term-identifier-benchmark-cases

## Why

The provider now has baseline retrieval evidence, query rewrite evidence, evidence grading candidates, and stress cases for insufficient evidence. The next retrieval risk is exact-term and identifier-heavy queries: policy codes, form names, workflow acronyms, and order-like ids often require lexical matching or hybrid retrieval, not only dense semantic similarity.

Before adding sparse vectors, BM25, hybrid query fusion, or rerankers, the project needs a local benchmark slice that records these exact-term scenarios and keeps them separate from the current baseline seed.

## What Changes

- Add exact-term and identifier-like business anchors to the local fixture sources.
- Add a dedicated exact-term benchmark fixture for policy codes, form names, workflow acronyms, and order-like identifiers.
- Add focused tests proving the fixture loads separately and remains runnable through the fixture backend.
- Export checked-in retrieval evidence for the exact-term fixture.
- Update README, research notes, architecture docs, and specs with the evidence boundary.

## Non-Goals

- Do not add hybrid retrieval, sparse vectors, BM25, or a reranker.
- Do not change `/api/rag/retrieve` behavior.
- Do not replace the main Chinese seed benchmark.
- Do not promote Qdrant or BGE-M3 to production.
- Do not change runtime defaults.

## Success Criteria

- Exact-term cases are maintained separately from the baseline seed.
- The fixture includes policy code, form name, workflow acronym, and order-like id categories.
- Focused and full tests pass.
- Exact-term retrieval evidence is exported as JSON and Markdown.
- The change is archived and main specs validate strictly.
