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
| fixture | 32 | 0.9062 | 0.9062 | 0.7500 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 12 | 0.7500 | 0.7500 | 0.7500 |
| evidence | 1 | 1.0000 | 1.0000 | 0.0000 |
| exception-policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| faq | 1 | 1.0000 | 1.0000 | 0.0000 |
| identifier-noise | 2 | 1.0000 | 1.0000 | 0.0000 |
| long-section | 2 | 1.0000 | 1.0000 | 0.0000 |
| multi-intent | 1 | 1.0000 | 1.0000 | 0.0000 |
| multi-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| operational-escalation | 2 | 1.0000 | 1.0000 | 0.0000 |
| paraphrase | 2 | 1.0000 | 1.0000 | 0.0000 |
| policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| policy-nuance | 4 | 1.0000 | 1.0000 | 0.0000 |
| sla | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| refund-delayed-shipping | policy | easy | true | true |  | 0.342 | refund_policy_2026#section-3, refund_policy_2026#exact-refund-code |
| logistics-delay | faq | easy | true | true |  | 0.184 | logistics_faq_2026#delay, logistics_faq_2026#batch-exception |
| empty-moon-warehouse | empty | easy | true | true | true | 0.157 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 0.164 | refund_policy_2026#section-3, refund_policy_2026#exact-refund-code |
| refund-evidence-records | evidence | easy | true | true |  | 0.158 | refund_policy_2026#section-5, refund_policy_2026#appeal-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 0.163 | logistics_faq_2026#delay, logistics_faq_2026#lost-package |
| multi-source-after-sales | multi-source | medium | true | true |  | 0.362 | refund_policy_2026#section-5, refund_policy_2026#appeal-review, logistics_faq_2026#batch-exception |
| refund-customized-exception | exception-policy | medium | true | true |  | 0.189 | refund_policy_2026#exception, refund_policy_2026#appeal-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 0.162 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 0.308 | refund_policy_2026#address-change, logistics_faq_2026#lost-package, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 0.322 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#batch-exception |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 0.388 | logistics_faq_2026#lost-package, logistics_faq_2026#batch-exception, logistics_faq_2026#delay |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 0.167 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| refund-appeal-second-review | long-section | hard | true | true |  | 0.210 | refund_policy_2026#appeal-review, refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |
| logistics-batch-exception-escalation | long-section | hard | true | true |  | 0.196 | logistics_faq_2026#batch-exception, logistics_faq_2026#lost-package, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | true | true | true | 0.294 |  |
| empty-invoice-tax-policy | empty | hard | true | true | true | 0.280 |  |
| empty-membership-tier-recovery | empty | medium | true | true | true | 0.271 |  |
| empty-coupon-approval | empty | medium | true | true | true | 0.268 |  |
| empty-password-reset-email | empty | medium | true | true | true | 0.291 |  |
| empty-finance-reconciliation | empty | hard | true | true | true | 0.268 |  |
| refund-high-value-review-customer-like | policy-nuance | hard | true | true |  | 0.184 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| empty-datacenter-temperature-alert | empty | medium | true | true | true | 0.283 |  |
| empty-social-security-reconciliation | empty | medium | true | true | true | 0.279 |  |
| refund-high-value-review-audit-trace-customer-like | policy-nuance | hard | true | true |  | 0.162 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| refund-high-value-review-customer-like-audit-trace-2 | policy-nuance | hard | true | true |  | 0.165 | refund_policy_2026#appeal-review, refund_policy_2026#high-value-review |
| logistics-exact-id-customer-like | identifier-noise | hard | true | true |  | 0.157 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception |
| empty-refund-high-value-auto-compensation | empty | hard | false | false | false | 0.287 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change |
| empty-refund-high-value-auto-compensation-customer-like-2 | empty | hard | false | false | false | 0.288 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change |
| refund-high-value-review-customer-like-v2 | policy-nuance | hard | true | true |  | 0.165 | refund_policy_2026#high-value-review, refund_policy_2026#appeal-review |
| logistics-exact-id-customer-like-v2 | identifier-noise | hard | true | true |  | 0.159 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception |
| empty-refund-high-value-cross-train-v2 | empty | hard | false | false | false | 0.305 | refund_policy_2026#high-value-review, refund_policy_2026#exact-refund-code, refund_policy_2026#address-change |
