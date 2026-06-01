# Phase 3 FP/FN Review Report

- Report: `phase3-fp-fn-review-v1`
- Generated At: `2026-06-01T03:35:58.390198+00:00`
- Source Benchmark Report: `docs\benchmark\chinese-seed\retrieval-candidates\fixture-chinese-seed-baseline.json`

## Summary

| Metric | Value |
|---|---|
| Total Cases | `32` |
| False Positive Count | `3` |
| False Negative Count | `0` |
| False Positive Rate | `0.0938` |
| False Negative Rate | `0.0000` |

## False Positive Cases

| Case ID | Category | Returned Citations |
|---|---|---|
| `empty-refund-high-value-auto-compensation` | `empty` | `refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change` |
| `empty-refund-high-value-auto-compensation-customer-like-2` | `empty` | `refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change` |
| `empty-refund-high-value-cross-train-v2` | `empty` | `refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change` |

## False Negative Cases

| Case ID | Category | Hit At K | Citation Match |
|---|---|---|---|
| `none` | `n/a` | `n/a` | `n/a` |

## Notes

- This report is a read-only review view over existing benchmark evidence.
- It does not change retrieval defaults, thresholds, or runtime promotion status.
