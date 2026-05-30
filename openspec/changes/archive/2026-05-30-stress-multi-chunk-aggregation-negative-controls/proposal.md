## Why

The first multi-chunk aggregation candidate recovered a split-chunk false negative, but it has not yet been tested against over-broad same-document grouping. Before any runtime promotion can be considered, the provider needs negative controls that prove aggregation can fail closed when a document contains related-looking but unsupported identifier combinations.

## What Changes

- Add expected-empty same-document benchmark cases for multi-chunk aggregation.
- Extend the existing multi-chunk aggregation evidence export path to combine positive split-chunk cases with negative controls.
- Export updated JSON and Markdown evidence showing both recovered positives and expected-empty behavior.
- Keep the work evaluation-only: no public HTTP API changes, no runtime retrieval default changes, no production parent-document store, no reranker, and no answer generation change.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `retrieval-benchmark-harness`: Adds negative-control fixtures and evidence requirements for multi-chunk aggregation candidates.
- `production-indexing-architecture`: Clarifies that aggregation promotion requires both positive recovery and same-document negative-control evidence.

## Impact

- Affected code: retrieval benchmark fixtures, aggregation export tests, generated benchmark evidence, README and architecture/research docs.
- APIs: No public HTTP API contract changes.
- Dependencies: No new dependencies.
- Systems: Local benchmark/export tooling only; runtime provider behavior remains unchanged.
