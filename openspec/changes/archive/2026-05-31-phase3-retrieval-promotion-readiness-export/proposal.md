## Why

The Phase 3 gap matrix is now documented, but reviewers still have to read it as a markdown file. We need a machine-readable readiness export so the same gate picture can be regenerated, compared, and surfaced in handoff without changing retrieval behavior.

## What Changes

- Add a local Phase 3 retrieval promotion readiness export that writes JSON and Markdown evidence files.
- Summarize the current promotion gates for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, relation-aware grading, and deployed smoke.
- Surface the readiness export through provider handoff and handoff refresh as optional review evidence.
- Keep the export read-only. It should report open gates, not close them automatically.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds an exportable Phase 3 readiness report.
- `knowledge-provider`: provider handoff and refresh can summarize the new readiness export as optional evidence.
- `provider-roadmap`: records the export as lightweight Phase 3 review visibility work.

## Impact

- Affected code: `app/services/phase3_retrieval_promotion_readiness.py` (new), `scripts/export_phase3_retrieval_promotion_readiness.py` (new)
- Affected tests: `tests/test_phase3_retrieval_promotion_readiness.py` (new), plus focused handoff bundle/refresh assertions
- Affected docs/evidence: `docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.json` and `.md`
- No runtime default changes, no new HTTP API, no new dependencies
