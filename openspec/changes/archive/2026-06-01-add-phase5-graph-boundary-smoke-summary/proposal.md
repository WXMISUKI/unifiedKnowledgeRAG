## Why

Phase 5 already has graph use-case readiness evidence and graph boundary discovery in provider preflight and provider contract smoke. Reviewers still have to open multiple artifacts to see the graph schema discovery signal and the planned graph query boundary together. We need a compact, read-only smoke summary that makes the graph boundary easy to review without adding GraphRAG execution.

## What Changes

- Add a local Phase 5 graph boundary smoke summary that consolidates graph schema discovery and the planned graph query boundary into one review artifact.
- Summarize graph count, graph ids, graph store labels, entity/relation type counts, and the `GRAPH_NOT_IMPLEMENTED` boundary in a compact report.
- Surface the smoke summary through provider handoff and handoff refresh as optional review evidence.
- Keep the summary read-only. It should report the current graph boundary, not promote GraphRAG execution.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records the summary as lightweight Phase 5 GraphRAG boundary/readiness work.
- `knowledge-provider`: provider handoff and refresh can summarize the new graph boundary smoke evidence as optional evidence.
- `retrieval-benchmark-harness`: adds an exportable Phase 5 graph boundary smoke summary report.

## Impact

- Affected code: `app/services/phase5_graph_boundary_smoke_summary.py` (new), `scripts/export_phase5_graph_boundary_smoke_summary.py` (new)
- Affected tests: `tests/test_phase5_graph_boundary_smoke_summary.py` (new), plus focused handoff bundle/refresh assertions
- Affected docs/evidence: `docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.json` and `.md`
- No runtime default changes, no new HTTP API, no new dependencies
