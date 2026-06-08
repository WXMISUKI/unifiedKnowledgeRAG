## Why

The current aggregate real-business golden-case baseline still proves only one successful source, which is not enough to guide the next retrieval maturity step without risking local over-optimization. We need one more real business source in the same evidence path so future chunking, query rewrite, rerank, hybrid, or GraphRAG work is chosen by observed failures rather than by technique popularity.

## What Changes

- Extend the aggregate local business golden-case fixture with a second real business source based on `refund_policy_docs`.
- Export refreshed aggregate JSON and Markdown evidence that summarize two real sources in one baseline.
- Add focused verification for multi-source aggregate `go`, `review`, and `blocked` behavior while preserving current single-source compatibility.
- Keep the slice evidence-only: no runtime default changes, no source binding creation, no MyPrivateAgent orchestration, no parser ownership expansion, and no advanced retrieval strategy promotion.

## Capabilities

### New Capabilities

### Modified Capabilities
- `local-business-rag-golden-cases`: Extend the aggregate baseline so it can carry a second real business source and produce source-aware aggregate evidence without changing runtime behavior.
- `provider-roadmap`: Record that the next maturity step after the first aggregate baseline is to append a second real business source before considering advanced retrieval strategy changes.

## Impact

- Updates the existing local business golden-case service/exporter inputs and aggregate evidence artifacts.
- Refreshes `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json` and `.md`.
- Adds focused tests around real multi-source aggregate coverage.
- Updates roadmap/progress documentation after the evidence refresh.
- No public HTTP API changes.
- No new external dependencies.
- No runtime retrieval default changes.
