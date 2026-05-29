# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| fixture | 4 | 1.0000 | 1.0000 | 0.0000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| form-name | 1 | 1.0000 | 1.0000 | 0.0000 |
| order-like-id | 1 | 1.0000 | 1.0000 | 0.0000 |
| policy-code | 1 | 1.0000 | 1.0000 | 0.0000 |
| workflow-acronym | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| exact-refund-policy-code | policy-code | medium | true | true |  | 0.341 | refund_policy_2026#exact-refund-code, refund_policy_2026#high-value-review |
| exact-refund-form-name | form-name | medium | true | true |  | 0.169 | refund_policy_2026#exact-refund-code, refund_policy_2026#appeal-review |
| exact-logistics-workflow-acronym | workflow-acronym | hard | true | true |  | 0.249 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception |
| exact-logistics-order-id | order-like-id | hard | true | true |  | 0.157 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception |
