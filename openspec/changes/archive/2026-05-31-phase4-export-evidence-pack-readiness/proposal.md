## Why

The Phase 4 evidence pack consumption contract is documented, but reviewers still have to inspect the contract note and the provider contract smoke evidence separately. We need a machine-readable readiness export that consolidates the current evidence-pack contract coverage, smoke coverage, and caller-facing review status without changing runtime behavior.

## What Changes

- Add a local Phase 4 evidence pack readiness export that writes JSON and Markdown evidence files.
- Summarize the stable `evidence_pack-v1` contract, provider contract smoke coverage, and the remaining caller-consumption review gaps.
- Surface the readiness export through provider handoff and handoff refresh as optional review evidence.
- Keep the export read-only. It should report readiness, not alter caller ownership or runtime defaults.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds an exportable Phase 4 evidence pack readiness report.
- `knowledge-provider`: provider handoff and refresh can summarize the new readiness export as optional evidence.
- `provider-roadmap`: records the export as lightweight Phase 4 evidence packaging work.

## Impact

- Affected code: `app/services/phase4_evidence_pack_readiness.py` (new), `scripts/export_phase4_evidence_pack_readiness.py` (new)
- Affected tests: `tests/test_phase4_evidence_pack_readiness.py` (new), plus focused handoff bundle/refresh assertions
- Affected docs/evidence: `docs/benchmark/chinese-seed/evidence-pack-readiness/phase4-evidence-pack-readiness.json` and `.md`
- No runtime default changes, no new HTTP API, no new dependencies
