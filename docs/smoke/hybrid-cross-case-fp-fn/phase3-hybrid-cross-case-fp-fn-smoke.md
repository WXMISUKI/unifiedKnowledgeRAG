# Phase 3 Hybrid Cross-Case FP/FN Smoke Report

- Report: `phase3-hybrid-cross-case-fp-fn-smoke-v1`
- Status: `passed`
- Generated At: `2026-06-03T01:40:57.604297+00:00`
- Baseline Source: `docs\benchmark\chinese-seed\retrieval-candidates\fixture-chinese-seed-baseline.json`
- FP/FN Source: `docs\benchmark\chinese-seed\fp-fn-review\phase3-fp-fn-review.json`
- Protocol Source: `docs\benchmark\chinese-seed\retrieval-candidate-evaluation-protocol\phase3-retrieval-candidate-evaluation-protocol.md`

## Summary

| Metric | Value |
|---|---|
| Total Checks | `4` |
| Passed Checks | `4` |
| Failed Checks | `0` |
| Baseline Total Cases | `32` |
| False Positive Count | `3` |
| False Negative Count | `0` |

## Checks

| Check | Scenario | Status | Details |
|---|---|---|---|
| `baseline_cross_case_coverage` | `baseline risk case ids are present` | `passed` | {"present_case_count": 4, "required_case_ids": ["empty-refund-high-value-auto-compensation", "empty-refund-high-value-auto-compensation-customer-like-2", "logistics-exact-id-customer-like", "refund-high-value-review-customer-like-audit-trace-2"]} |
| `false_positive_alignment` | `fp review contains expected empty trap cases` | `passed` | {"expected_false_positive_ids": ["empty-refund-high-value-auto-compensation", "empty-refund-high-value-auto-compensation-customer-like-2"], "observed_false_positive_count": 3} |
| `positive_control_and_fn_guard` | `positive controls remain successful while fn count stays zero` | `passed` | {"false_negative_count": 0, "positive_control_ids": ["logistics-exact-id-customer-like", "refund-high-value-review-customer-like-audit-trace-2"]} |
| `evaluation_protocol_artifact` | `phase3 evaluation protocol is present` | `passed` | {"path": "docs\\benchmark\\chinese-seed\\retrieval-candidate-evaluation-protocol\\phase3-retrieval-candidate-evaluation-protocol.md", "present": true} |

## Notes

- This smoke validates cross-case FP/FN signal visibility from existing local evidence.
- It is read-only and does not execute retrieval backends.
- Smoke readiness reflects evidence integrity, not runtime promotion approval.
