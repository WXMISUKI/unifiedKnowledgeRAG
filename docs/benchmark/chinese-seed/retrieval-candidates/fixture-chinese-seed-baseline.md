# Retrieval Candidate Evaluation

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| fixture-chinese-seed-baseline | fixture | Fixture baseline for the local Chinese benchmark seed; contract evidence only, not semantic retrieval quality. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_seed | chinese-enterprise-support-v1 |
| embedding | none |
| quality_claim | contract-baseline-only |
| vector_store | none |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| fixture | 26 | 0.9615 | 0.9615 | 0.9000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 10 | 0.9000 | 0.9000 | 0.9000 |
| evidence | 1 | 1.0000 | 1.0000 | 0.0000 |
| exception-policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| faq | 1 | 1.0000 | 1.0000 | 0.0000 |
| long-section | 2 | 1.0000 | 1.0000 | 0.0000 |
| multi-intent | 1 | 1.0000 | 1.0000 | 0.0000 |
| multi-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| operational-escalation | 2 | 1.0000 | 1.0000 | 0.0000 |
| paraphrase | 2 | 1.0000 | 1.0000 | 0.0000 |
| policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| policy-nuance | 2 | 1.0000 | 1.0000 | 0.0000 |
| sla | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| refund-delayed-shipping | policy | easy | true | true |  | 0.575 | refund_policy_2026#section-3, refund_policy_2026#exact-refund-code |
| logistics-delay | faq | easy | true | true |  | 0.377 | logistics_faq_2026#delay, logistics_faq_2026#batch-exception |
| empty-moon-warehouse | empty | easy | true | true | true | 0.295 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 0.330 | refund_policy_2026#section-3, refund_policy_2026#exact-refund-code |
| refund-evidence-records | evidence | easy | true | true |  | 0.314 | refund_policy_2026#section-5, refund_policy_2026#appeal-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 0.267 | logistics_faq_2026#delay, logistics_faq_2026#lost-package |
| multi-source-after-sales | multi-source | medium | true | true |  | 0.601 | refund_policy_2026#section-5, refund_policy_2026#appeal-review, logistics_faq_2026#batch-exception |
| refund-customized-exception | exception-policy | medium | true | true |  | 0.280 | refund_policy_2026#exception, refund_policy_2026#appeal-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 0.254 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 0.367 | refund_policy_2026#address-change, logistics_faq_2026#lost-package, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 0.148 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#batch-exception |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 0.284 | logistics_faq_2026#lost-package, logistics_faq_2026#batch-exception, logistics_faq_2026#delay |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 0.146 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| refund-appeal-second-review | long-section | hard | true | true |  | 0.178 | refund_policy_2026#appeal-review, refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |
| logistics-batch-exception-escalation | long-section | hard | true | true |  | 0.217 | logistics_faq_2026#batch-exception, logistics_faq_2026#lost-package, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | true | true | true | 0.282 |  |
| empty-invoice-tax-policy | empty | hard | true | true | true | 0.264 |  |
| empty-membership-tier-recovery | empty | medium | true | true | true | 0.350 |  |
| empty-coupon-approval | empty | medium | true | true | true | 0.272 |  |
| empty-password-reset-email | empty | medium | true | true | true | 0.307 |  |
| empty-finance-reconciliation | empty | hard | true | true | true | 0.294 |  |
| refund-high-value-review-customer-like | policy-nuance | hard | true | true |  | 0.199 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| empty-datacenter-temperature-alert | empty | medium | true | true | true | 0.355 |  |
| empty-social-security-reconciliation | empty | medium | true | true | true | 0.477 |  |
| refund-high-value-review-audit-trace-customer-like | policy-nuance | hard | true | true |  | 0.277 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| empty-refund-high-value-auto-compensation | empty | hard | false | false | false | 0.662 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change |
