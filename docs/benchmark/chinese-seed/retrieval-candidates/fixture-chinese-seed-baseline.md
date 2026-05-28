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
| fixture | 15 | 1.0000 | 1.0000 | 1.0000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 3 | 1.0000 | 1.0000 | 1.0000 |
| evidence | 1 | 1.0000 | 1.0000 | 0.0000 |
| exception-policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| faq | 1 | 1.0000 | 1.0000 | 0.0000 |
| multi-intent | 1 | 1.0000 | 1.0000 | 0.0000 |
| multi-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| operational-escalation | 2 | 1.0000 | 1.0000 | 0.0000 |
| paraphrase | 2 | 1.0000 | 1.0000 | 0.0000 |
| policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| sla | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| refund-delayed-shipping | policy | easy | true | true |  | 0.227 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | 0.101 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | true | true | true | 0.085 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 0.102 | refund_policy_2026#section-3, refund_policy_2026#section-5 |
| refund-evidence-records | evidence | easy | true | true |  | 0.087 | refund_policy_2026#section-5, refund_policy_2026#section-3 |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 0.083 | logistics_faq_2026#delay, logistics_faq_2026#lost-package |
| multi-source-after-sales | multi-source | medium | true | true |  | 0.158 | refund_policy_2026#section-5, refund_policy_2026#section-3, refund_policy_2026#high-value-review |
| refund-customized-exception | exception-policy | medium | true | true |  | 0.087 | refund_policy_2026#exception, refund_policy_2026#section-3 |
| refund-high-value-review | operational-escalation | medium | true | true |  | 0.085 | refund_policy_2026#high-value-review, refund_policy_2026#section-3 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 0.387 | refund_policy_2026#address-change, logistics_faq_2026#lost-package, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 0.115 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 0.165 | logistics_faq_2026#lost-package, logistics_faq_2026#delay, logistics_faq_2026#address-intercept |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 0.082 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | true | true | true | 0.142 |  |
| empty-invoice-tax-policy | empty | hard | true | true | true | 0.138 |  |
