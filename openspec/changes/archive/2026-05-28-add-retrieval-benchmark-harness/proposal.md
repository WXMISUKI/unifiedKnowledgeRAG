## Why

Production embedding and vector database choices should be evidence-driven. The provider needs a small benchmark harness that can run the same retrieval cases against existing and future retrieval backends before we choose production infrastructure.

## What Changes

- Add a local retrieval benchmark harness with structured benchmark cases.
- Evaluate existing fixture and LlamaIndex backends through the existing retriever abstraction.
- Report `hit_at_k`, `citation_match`, `empty_query_handling`, and latency metrics.
- Keep the first interface service/CLI-test oriented; no new public operator API in this slice.
- Do not add production embedding models, vector databases, rerankers, or external benchmark dependencies.

## Capabilities

### New Capabilities

- `retrieval-benchmark-harness`: Local retrieval benchmark cases, metrics, and reports for comparing retrieval adapters.

### Modified Capabilities

- `production-indexing-architecture`: Production infrastructure decisions should reference benchmark evidence before final implementation.

## Impact

- Adds benchmark case fixture data under `tests/fixtures`.
- Adds `app/services/retrieval_benchmark.py`.
- Adds tests for benchmark metrics and report shape.
- Updates README and production indexing architecture docs with the benchmark workflow.
- Keeps existing retrieval APIs unchanged.
