## Context

`local-business-rag-golden-cases` now proves that the company-profile corpus can answer a small set of business questions and fail closed on unrelated questions. That is useful, but still too narrow to justify advanced RAG changes. The next step is to let the same evidence shape accept additional real sources or real failed questions, then classify failures before choosing a technique.

## Goals / Non-Goals

**Goals:**

- Add a multi-source case fixture format.
- Keep the existing single-source baseline valid.
- Add failure-mode fields to case inputs and aggregate summaries.
- Export one aggregate report that includes per-source case outcomes and chunk-quality diagnostics.
- Produce `go`, `review`, or `blocked` without changing runtime behavior.

**Non-Goals:**

- No query rewrite, HyDE, HyPE, rerank, hybrid retrieval, RAPTOR, Self/Corrective RAG, or GraphRAG implementation.
- No Qdrant, pgvector, BGE-M3, or vector backend promotion.
- No parser engine ownership changes.
- No MyPrivateAgent orchestration or source binding.
- No new public HTTP APIs.

## Decisions

1. **Add an aggregate wrapper instead of replacing the existing exporter.**
   - Rationale: The current single-source baseline is already useful and tested. A wrapper can group cases by source, reuse existing retrieval/answer checks, and reduce regression risk.
   - Alternative considered: Rewrite `export_local_business_rag_golden_cases` to be multi-source-only. That would make the previous report less stable and invite unnecessary churn.

2. **Use fixture-declared failure modes rather than automatic diagnosis.**
   - Rationale: The provider can record whether a question is suspected parser/OCR, chunking, query mismatch, retrieval quality, citation/evidence, availability, or caller/operator flow, but it should not pretend to infer root cause automatically.
   - Alternative considered: Derive failure mode from scores/citations. That is brittle and would be premature for this lightweight provider.

3. **Keep aggregation evidence-only.**
   - Rationale: The aggregate report should guide future OpenSpec changes, not change the current retrieval path.
   - Alternative considered: Auto-route to different retrieval strategies by failure type. That crosses into runtime orchestration and is explicitly out of scope.

## Risks / Trade-offs

- **Risk: Multi-source fixture still contains only one source initially.** -> Mitigation: The format supports multiple sources immediately, and the first checked-in fixture reuses the existing source as a compatibility baseline.
- **Risk: Failure-mode labels can be subjective.** -> Mitigation: Treat labels as review hints and keep decision based on observable case outcomes.
- **Risk: Aggregate reports become another evidence chain to maintain.** -> Mitigation: Keep one command, one output directory, and avoid adding it to provider handoff refresh until a real consumer needs it.
- **Risk: Users may interpret `go` as production promotion.** -> Mitigation: Report non-goals and runtime-promotion status explicitly.
