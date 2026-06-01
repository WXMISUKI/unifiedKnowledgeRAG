# Phase 4 Caller Consumption Smoke Report

- Report: `phase4-caller-consumption-smoke-v1`
- Status: `passed`
- Generated At: `2026-06-01T08:51:05.437557+00:00`
- Contract Doc: `docs\benchmark\chinese-seed\evidence-pack-consumption-contract\phase4-evidence-pack-consumption-contract.md`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `3` |
| Passed Checks | `3` |
| Failed Checks | `0` |
| Answerable Checks | `1` |
| Insufficient Checks | `1` |
| Contract Doc Present | `1` |

## Checks

| Check | Scenario | Status | Details |
|---|---|---|---|
| `caller_allowlist_rule` | `build_evidence_pack(answerable)` | `passed` | {"allowed_citations": ["refund_policy_2026#section-3", "logistics_2026#section-2"], "citation_policy": "use_only_returned_citations", "evidence_count": 2, "reason": "documents_returned", "status": "answerable", "version": "evidence-pack-v1"} |
| `caller_fail_closed_rule` | `build_evidence_pack(insufficient_evidence)` | `passed` | {"allowed_citations": 0, "evidence_count": 0, "reason": "no_documents", "status": "insufficient_evidence", "version": "evidence-pack-v1"} |
| `caller_contract_artifact` | `docs/benchmark/chinese-seed/evidence-pack-consumption-contract` | `passed` | {"contract_path": "docs\\benchmark\\chinese-seed\\evidence-pack-consumption-contract\\phase4-evidence-pack-consumption-contract.md", "present": true} |

## Notes

- This smoke is local, read-only caller-consumption evidence.
- It exercises build_evidence_pack directly instead of re-running provider HTTP flow.
- It complements the provider contract smoke and the Phase 4 readiness export.
