## Design Overview

This is a documentation-only execution contract for live URL validation.

Inputs:

1. deployed provider base URL
2. optional provider API key
3. existing local deployment/handoff evidence context

Output:

- `phase8-live-url-validation-execution-contract.md`

## Contract Scope

- Execution preconditions for running deployed smoke against a real URL
- Allowed endpoint list (read-only discovery and handoff endpoints)
- Status semantics (`ready/review/blocked`) for live validation interpretation
- Boundary rules: live validation does not imply runtime default promotion

## Boundaries

- No runtime default promotion
- No retrieval or answer execution
- No ingestion, reindex, or GraphRAG execution
- No control-plane ownership transfer
