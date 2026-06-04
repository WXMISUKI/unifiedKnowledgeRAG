# Phase 3 Aggregation Relation Negative-Control Smoke Report

- Report: `phase3-aggregation-relation-negative-control-smoke-v1`
- Status: `ready`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-04T03:48:11.402504+00:00`
- Aggregation Candidate Source: `docs\benchmark\chinese-seed\multi-chunk-aggregation-candidates\qdrant-bge-m3-hybrid-multi-chunk-aggregation.json`
- Aggregation Negative-Control Source: `docs\benchmark\chinese-seed\multi-chunk-aggregation-negative-controls\qdrant-bge-m3-hybrid-multi-chunk-aggregation.json`
- Relation-Aware Grading Source: `docs\benchmark\chinese-seed\relation-aware-aggregation-grading\relation-aware-aggregation-grading.json`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `4` |
| Passed Checks | `4` |
| Failed Checks | `0` |
| Open Check IDs | `[]` |

## Checks

| Check | Status | Summary | Recommended Action |
|---|---|---|---|
| `aggregation_positive_control` | `ready` | backend=qdrant-hybrid:source-document-identifier-coverage-v1; total_cases=1; hit_rate=1.0000; citation_match_rate=1.0000; split_case_hit_at_k=True | `no_action_required` |
| `aggregation_negative_control` | `ready` | backend=qdrant-hybrid:source-document-identifier-coverage-v1; total_cases=2; hit_rate=0.5000; citation_match_rate=0.5000; empty_handling_rate=0.0000; negative_case_hit_at_k=False | `no_action_required` |
| `relation_aware_labeling` | `ready` | candidate=relation-aware-aggregation-grader-v1; label=relation_unsupported; reason=Returned evidence contains identifiers but does not prove the requested relationship. | `no_action_required` |
| `relation_aware_summary` | `ready` | total_cases=2; answer_bearing_rate=1.0000; relation_unsupported_count=1; unexpected_evidence_count=0; expected_empty_pass_rate=1.0000 | `no_action_required` |

## Notes

- This smoke reuses existing aggregation and relation-aware grading evidence.
- It is read-only and does not execute retrieval backends.
- Smoke readiness reflects negative-control visibility, not runtime promotion approval.
