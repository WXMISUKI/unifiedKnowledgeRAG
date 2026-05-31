## Why

The Phase 5 graph use-case readiness contract is documented, but reviewers still have to read the contract and the existing graph boundary evidence separately. We need a machine-readable readiness export that consolidates the current graph use-case contract, graph schema discovery, and planned boundary evidence without changing runtime behavior.

## What Changes

- Add a local Phase 5 graph use-case readiness export that writes JSON and Markdown evidence files.
- Summarize the graph use-case contract, provider preflight graph boundary, and provider contract smoke graph boundary checks.
- Surface the readiness export through provider handoff and handoff refresh as optional review evidence.
- Keep the export read-only. It should report the current Phase 5 boundary, not promote GraphRAG execution.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records the export as lightweight Phase 5 GraphRAG boundary/readiness work.
- `knowledge-provider`: provider handoff and refresh can summarize the new readiness export as optional evidence.
- `retrieval-benchmark-harness`: adds an exportable Phase 5 graph use-case readiness report.

## Impact

- Affected code: `app/services/phase5_graph_use_case_readiness.py` (new), `scripts/export_phase5_graph_use_case_readiness.py` (new)
- Affected tests: `tests/test_phase5_graph_use_case_readiness.py` (new), plus focused handoff bundle/refresh assertions
- Affected docs/evidence: `docs/benchmark/chinese-seed/graph-use-case-readiness/phase5-graph-use-case-readiness.json` and `.md`
- No runtime default changes, no new HTTP API, no new dependencies
