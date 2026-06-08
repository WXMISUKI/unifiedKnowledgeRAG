## Why

The provider now has a reusable company-profile golden-case baseline, but relying on one successful document can still lead to local over-optimization. The next maturity step is to support more real business documents or real failed questions in the same baseline, so future RAG strategy changes are triggered by observed failure modes rather than by generic technique popularity.

## What Changes

- Extend the local business RAG golden-case baseline to support a multi-source case fixture.
- Add failure-mode classification fields for real questions and real failures.
- Export an aggregate JSON and Markdown report that summarizes per-source case outcomes and chunk-quality diagnostics.
- Preserve the existing single-source company-profile baseline as a valid input.
- Keep the report evidence-only: no runtime default changes, no backend promotion, no source binding, no MyPrivateAgent orchestration, and no GraphRAG execution.

## Capabilities

### New Capabilities

### Modified Capabilities
- `local-business-rag-golden-cases`: Extend the existing local business golden-case baseline to support multi-source cases, failure-mode classification, and aggregate source/case/chunk-quality summaries.
- `provider-roadmap`: Record that future mature RAG work should add real documents or real failed questions to this baseline before proposing advanced retrieval or GraphRAG techniques.

## Impact

- Updates the existing local business golden-case service/exporter or adds a small aggregate wrapper.
- Adds a multi-source case fixture under `docs/local-run/business-rag-golden-cases/`.
- Adds focused tests for multi-source `go`, `review`, and `blocked` decisions.
- Updates roadmap/progress documentation after evidence export.
- No public HTTP API changes.
- No new external dependencies.
- No runtime retrieval default changes.
