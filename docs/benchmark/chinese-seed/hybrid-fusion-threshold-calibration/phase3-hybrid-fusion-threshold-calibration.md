# Phase 3 Hybrid Fusion Threshold Calibration

- Report: `phase3-hybrid-fusion-threshold-calibration-v1`
- Status: `review`
- Decision: `keep_runtime_defaults`
- Generated At: `2026-06-01T03:35:58.405942+00:00`

## Summary

| Metric | Value |
|---|---|
| Total Signals | `6` |
| Ready Signals | `3` |
| Review Signals | `3` |
| Blocked Signals | `0` |
| Open Signal IDs | `["hybrid_empty_stress_negative_control", "cross_case_fp_fn_context", "runtime_threshold_alignment"]` |

## Calibration

| Metric | Value |
|---|---|
| Fusion Mode | `rrf` |
| Score Filter Mode | `disabled-for-rrf-fusion-score` |
| Dense Selected Threshold | `0.7` |
| Runtime Threshold | `0.01` |
| Threshold Delta | `0.69` |
| Sweep Threshold Count | `3` |
| Sweep Best Empty Handling Rate | `1.0` |
| Hybrid Exact-Term Hit Rate | `1.0` |
| Hybrid Empty-Stress Empty Handling Rate | `0.0` |

## Signals

| Signal | Status | Summary | Recommended Action |
|---|---|---|---|
| `hybrid_exact_term_positive_control` | `ready` | hit_rate=1.0000; total_cases=4 | `no_action_required` |
| `hybrid_empty_stress_negative_control` | `review` | empty_handling_rate=0.0000; total_cases=4 | `review_empty_false_positive_risk` |
| `hybrid_gate_coverage_bundle` | `ready` | present_gate_artifacts=4/4 | `no_action_required` |
| `dense_threshold_sweep_context` | `ready` | selected_dense_threshold=0.7000; sweep_threshold_count=3 | `no_action_required` |
| `cross_case_fp_fn_context` | `review` | false_positive_count=3; false_negative_count=0 | `continue_cross_case_fp_fn_review` |
| `runtime_threshold_alignment` | `review` | selected_dense_threshold=0.7000; runtime_threshold=0.0100; fusion=rrf; score_filter=disabled-for-rrf-fusion-score | `keep_runtime_defaults_until_hybrid_runtime_calibration` |

## Notes

- This report is local, read-only candidate calibration evidence for Phase 3 promotion review.
- Hybrid retrieval in these artifacts uses RRF fusion and score filtering is disabled for fusion scores.
- Dense threshold recommendations and runtime thresholds are not direct promotion instructions for hybrid RRF runtime defaults.
