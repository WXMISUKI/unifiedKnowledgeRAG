## Context

The provider now has a local fixture backend, a LlamaIndex backend, and a production indexing architecture decision record. The decision record says future production choices should be evidence-driven. A benchmark harness is the smallest useful implementation slice because it creates comparable measurements without committing to a specific embedding model or vector store.

## Goals / Non-Goals

**Goals:**

- Define benchmark cases in structured data.
- Run cases against a selected retrieval backend through `create_document_retriever(settings)`.
- Measure whether expected citations appear in top-k results.
- Measure whether expected source ids appear in top-k results.
- Measure empty retrieval behavior.
- Capture basic latency per case and aggregate summary.

**Non-Goals:**

- No production model/vector DB integration.
- No benchmark UI or public API.
- No statistical evaluation suite.
- No reranker evaluation in this slice.

## Decisions

1. Store cases as JSON.

   JSON keeps cases portable and makes later CLI/API/UI work straightforward.

2. Reuse existing retriever abstraction.

   Benchmarking should exercise the same contract path as retrieval code, so future adapters can be compared by swapping settings.

3. Report simple metrics first.

   `hit_at_k`, `citation_match`, and empty handling are easy to understand and sufficient for early adapter comparison.

4. Keep benchmark service pure Python.

   Tests can invoke it directly. A CLI or API can be added later when the benchmark set stabilizes.

## Risks / Trade-offs

- Small fixture benchmark can overfit -> acceptable as a harness seed; production decisions require real corpus cases later.
- Latency in unit tests is noisy -> use it as reported metadata, not a pass/fail threshold.
- Citation expectations depend on chunking -> useful because citation stability is a core provider contract.

## Migration Plan

1. Add case schema and fixture cases.
2. Add benchmark service and metrics.
3. Add focused tests.
4. Update docs.
5. Validate and archive.
