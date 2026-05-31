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
| fixture | 29 | 0.9310 | 0.9310 | 0.8182 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 11 | 0.8182 | 0.8182 | 0.8182 |
| evidence | 1 | 1.0000 | 1.0000 | 0.0000 |
| exception-policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| faq | 1 | 1.0000 | 1.0000 | 0.0000 |
| identifier-noise | 1 | 1.0000 | 1.0000 | 0.0000 |
| long-section | 2 | 1.0000 | 1.0000 | 0.0000 |
| multi-intent | 1 | 1.0000 | 1.0000 | 0.0000 |
| multi-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| operational-escalation | 2 | 1.0000 | 1.0000 | 0.0000 |
| paraphrase | 2 | 1.0000 | 1.0000 | 0.0000 |
| policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| policy-nuance | 3 | 1.0000 | 1.0000 | 0.0000 |
| sla | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| refund-delayed-shipping | policy | easy | true | true |  | 0.310 | refund_policy_2026#section-3, refund_policy_2026#exact-refund-code |
| logistics-delay | faq | easy | true | true |  | 0.197 | logistics_faq_2026#delay, logistics_faq_2026#batch-exception |
| empty-moon-warehouse | empty | easy | true | true | true | 0.157 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 0.161 | refund_policy_2026#section-3, refund_policy_2026#exact-refund-code |
| refund-evidence-records | evidence | easy | true | true |  | 0.149 | refund_policy_2026#section-5, refund_policy_2026#appeal-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 0.156 | logistics_faq_2026#delay, logistics_faq_2026#lost-package |
| multi-source-after-sales | multi-source | medium | true | true |  | 0.288 | refund_policy_2026#section-5, refund_policy_2026#appeal-review, logistics_faq_2026#batch-exception |
| refund-customized-exception | exception-policy | medium | true | true |  | 0.149 | refund_policy_2026#exception, refund_policy_2026#appeal-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 0.144 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 0.281 | refund_policy_2026#address-change, logistics_faq_2026#lost-package, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 0.144 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#batch-exception |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 0.279 | logistics_faq_2026#lost-package, logistics_faq_2026#batch-exception, logistics_faq_2026#delay |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 0.147 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| refund-appeal-second-review | long-section | hard | true | true |  | 0.168 | refund_policy_2026#appeal-review, refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |
| logistics-batch-exception-escalation | long-section | hard | true | true |  | 0.155 | logistics_faq_2026#batch-exception, logistics_faq_2026#lost-package, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | true | true | true | 0.260 |  |
| empty-invoice-tax-policy | empty | hard | true | true | true | 0.257 |  |
| empty-membership-tier-recovery | empty | medium | true | true | true | 0.251 |  |
| empty-coupon-approval | empty | medium | true | true | true | 0.249 |  |
| empty-password-reset-email | empty | medium | true | true | true | 0.251 |  |
| empty-finance-reconciliation | empty | hard | true | true | true | 0.250 |  |
| refund-high-value-review-customer-like | policy-nuance | hard | true | true |  | 0.161 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| empty-datacenter-temperature-alert | empty | medium | true | true | true | 0.314 |  |
| empty-social-security-reconciliation | empty | medium | true | true | true | 0.312 |  |
| refund-high-value-review-audit-trace-customer-like | policy-nuance | hard | true | true |  | 0.170 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| refund-high-value-review-customer-like-audit-trace-2 | policy-nuance | hard | true | true |  | 0.172 | refund_policy_2026#appeal-review, refund_policy_2026#high-value-review |
| logistics-exact-id-customer-like | identifier-noise | hard | true | true |  | 0.155 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception |
| empty-refund-high-value-auto-compensation | empty | hard | false | false | false | 0.296 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change |
| empty-refund-high-value-auto-compensation-customer-like-2 | empty | hard | false | false | false | 0.279 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change |
