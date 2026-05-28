## Why

The current retrieval benchmark harness proves the mechanics with three smoke cases, but it is too small to guide future embedding, vector database, hybrid retrieval, or reranker decisions. We need a broader local benchmark set that covers representative Chinese business retrieval patterns before comparing candidate adapters.

## What Changes

- Expand benchmark cases to cover policy, FAQ, evidence/receipt rules, paraphrased questions, multi-source queries, and explicit empty retrieval.
- Add metadata to benchmark cases so reports can group results by category and difficulty.
- Extend benchmark reports with category-level summary metrics.
- Keep the harness local and dependency-free.
- Do not change production retrieval behavior, embedding models, vector databases, or rerankers.

## Capabilities

### New Capabilities

### Modified Capabilities

- `retrieval-benchmark-harness`: Benchmark cases and reports become representative enough for early adapter comparison.

## Impact

- Updates `tests/fixtures/retrieval_benchmark_cases.json`.
- Extends `app/services/retrieval_benchmark.py` with case metadata and category summaries.
- Adds tests for expanded cases and category metrics.
- Updates README and production indexing architecture docs.
