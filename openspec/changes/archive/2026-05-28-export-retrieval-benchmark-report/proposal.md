## Why

The retrieval benchmark harness now produces useful in-memory metrics, but future embedding/vector/reranker comparisons need durable evidence files. Exporting JSON and Markdown reports makes benchmark runs reviewable, shareable, and comparable across candidate adapters.

## What Changes

- Add local benchmark report export helpers for JSON and Markdown.
- Preserve the current service-only benchmark workflow; no public API is added.
- Include summary metrics, category summaries, and per-case results in exported reports.
- Document report paths and intended use for future production infrastructure decisions.

## Capabilities

### New Capabilities

### Modified Capabilities

- `retrieval-benchmark-harness`: Benchmark reports can be exported as durable JSON and Markdown evidence files.
- `production-indexing-architecture`: Production retrieval infrastructure decisions should reference exported benchmark reports when available.

## Impact

- Extends `app/services/retrieval_benchmark.py`.
- Adds tests for JSON and Markdown report export.
- Updates README and production indexing architecture docs.
- Does not add external dependencies, APIs, or new model/vector integrations.
