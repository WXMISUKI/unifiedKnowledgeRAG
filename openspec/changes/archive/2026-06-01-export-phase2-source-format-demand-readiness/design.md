## Design Overview

This change introduces a read-only Phase 2 readiness report that consumes two existing evidence inputs:

1. `docs/operations/source-format-demand/phase2-parser-expansion-demand-contract.md`
2. `docs/integration/source-bindings/provider-source-bindings.json`

The service computes:

- source-level format posture (`markdown_only_sources`, `non_markdown_sources`)
- parser readiness totals (`parser_ready_documents`, `unsupported_documents`)
- demand signal (`format_expansion_demand_signal`)
- open expansion gate hints (`open_gate_ids`)

## Status Rules

- `blocked`: required contract or source-binding evidence missing/blocking.
- `review`: required evidence is present but demand signal is visible or source binding itself is in review.
- `ready`: required evidence is present and current corpus still cleanly matches Markdown baseline.

## Boundaries

- No parser runtime behavior changes.
- No ingestion job execution.
- No retrieval/default/runtime promotion.
- No control-plane policy changes.
