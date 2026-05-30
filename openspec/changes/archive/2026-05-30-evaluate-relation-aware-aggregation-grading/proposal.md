## Why

Multi-chunk aggregation can recover split evidence, but negative controls show source-document grouping is too broad for unsupported relationships. The next lightweight step is to evaluate a relation-aware grading candidate before considering rerankers, graph checks, or runtime aggregation.

## What Changes

- Add an evaluation-only relation-aware grading candidate for multi-chunk aggregation evidence.
- Export JSON and Markdown evidence that labels recovered positives and unsupported relation negatives.
- Add CLI support for exporting the relation grading report.
- Keep runtime behavior unchanged: no HTTP API changes, no default retrieval changes, no reranker, no LLM, and no GraphRAG execution.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `retrieval-benchmark-harness`: Adds relation-aware grading evidence for multi-chunk aggregation candidates.
- `production-indexing-architecture`: Records that relation-aware evidence is required before runtime aggregation promotion.

## Impact

- Affected code: retrieval benchmark service, Qdrant+BGE smoke export script, benchmark tests, generated benchmark evidence, README and architecture/research docs.
- APIs: No public HTTP API contract changes.
- Dependencies: No new dependencies.
- Systems: Local evaluation tooling only; runtime provider behavior remains unchanged.
