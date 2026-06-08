## Why

The second real-source aggregate baseline now exposes a real `review` result on `refund_policy_docs`, but the current report still mixes two different concerns: negative-control leakage and markdown chunk/provenance diagnostics. We need one small classification slice that turns these review signals into explicit failure categories before choosing any implementation change, so the project does not drift into local optimization.

## What Changes

- Refine the local business aggregate review output so `refund_policy_docs` review signals are classified into explicit failure observations.
- Add minimal fixture coverage for stricter refund-policy negative controls and markdown provenance interpretation.
- Export refreshed aggregate evidence and recommended next-step hints without changing runtime retrieval defaults.
- Keep the slice evidence-first: no query rewrite, no rerank, no hybrid retrieval, no GraphRAG, no parser ownership change, and no source-binding behavior changes.

## Capabilities

### New Capabilities

### Modified Capabilities
- `local-business-rag-golden-cases`: Extend local and aggregate golden-case reporting so review outcomes can distinguish negative-control leakage from markdown provenance/chunk-diagnostic mismatch.
- `provider-roadmap`: Record that when second-source aggregate evidence is `review`, the next slice should classify the failure before proposing retrieval strategy or chunking changes.

## Impact

- Updates the existing local business golden-case reporting logic and aggregate evidence artifact shape.
- Refreshes `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json` and `.md`.
- Adds focused tests for classified review reasons and conservative recommendation behavior.
- Updates roadmap/progress documentation after the evidence refresh.
- No public HTTP API changes.
- No new external dependencies.
- No runtime retrieval default changes.
