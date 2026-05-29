# Qdrant BGE-M3 Chunking Comparison Evidence

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T15:04:37.617049+00:00 |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| rag_score_threshold | 0.7 |
| source_ids | refund_policy_docs, logistics_faq |

## Strategy Summary

| Strategy | Chunk Count | Hit Rate | Citation Match Rate | Empty Handling Rate | Long-Section Hit Rate | Long-Section Citation Match Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| markdown-paragraph-v1 | 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| markdown-section-v1 | 2 | 0.6667 | 0.3333 | 1.0000 | 0.5000 | 0.0000 |
| token-window-v1 | 8 | 0.7619 | 0.3333 | 1.0000 | 0.5000 | 0.0000 |

## Case Results By Strategy

### markdown-paragraph-v1

| Case | Category | Hit@K | Citation Match | Empty Handling | Returned Citations |
| --- | --- | --- | --- | --- | --- |
| refund-delayed-shipping | policy | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | true | true |  | logistics_faq_2026#delay |
| empty-moon-warehouse | empty | true | true | true |  |
| refund-delivery-paraphrase | paraphrase | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | true | true |  | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | true | true |  | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | true | true |  | refund_policy_2026#section-5, refund_policy_2026#address-change |
| refund-customized-exception | exception-policy | true | true |  | refund_policy_2026#exception |
| refund-high-value-review | operational-escalation | true | true |  | refund_policy_2026#high-value-review |
| refund-address-change-before-shipping | multi-intent | true | true |  | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | true | true |  | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | true | true |  | logistics_faq_2026#lost-package |
| logistics-address-intercept | operational-escalation | true | true |  | logistics_faq_2026#address-intercept |
| refund-appeal-second-review | long-section | true | true |  | refund_policy_2026#appeal-review, refund_policy_2026#address-change, refund_policy_2026#section-5 |
| logistics-batch-exception-escalation | long-section | true | true |  | logistics_faq_2026#batch-exception |
| empty-membership-points | empty | true | true | true |  |
| empty-invoice-tax-policy | empty | true | true | true |  |
| empty-membership-tier-recovery | empty | true | true | true |  |
| empty-coupon-approval | empty | true | true | true |  |
| empty-password-reset-email | empty | true | true | true |  |
| empty-finance-reconciliation | empty | true | true | true |  |

### markdown-section-v1

| Case | Category | Hit@K | Citation Match | Empty Handling | Returned Citations |
| --- | --- | --- | --- | --- | --- |
| refund-delayed-shipping | policy | true | false |  | refund_policy_2026#section-candidate |
| logistics-delay | faq | true | false |  | logistics_faq_2026#section-candidate |
| empty-moon-warehouse | empty | true | true | true |  |
| refund-delivery-paraphrase | paraphrase | true | false |  | refund_policy_2026#section-candidate |
| refund-evidence-records | evidence | false | false |  |  |
| logistics-carrier-paraphrase | paraphrase | false | false |  |  |
| multi-source-after-sales | multi-source | false | false |  |  |
| refund-customized-exception | exception-policy | false | false |  |  |
| refund-high-value-review | operational-escalation | false | false |  |  |
| refund-address-change-before-shipping | multi-intent | true | false |  | refund_policy_2026#section-candidate |
| logistics-same-city-timeout | sla | true | false |  | logistics_faq_2026#section-candidate |
| logistics-lost-package-cross-team | cross-source | true | false |  | logistics_faq_2026#section-candidate |
| logistics-address-intercept | operational-escalation | false | false |  |  |
| refund-appeal-second-review | long-section | false | false |  |  |
| logistics-batch-exception-escalation | long-section | true | false |  | logistics_faq_2026#section-candidate |
| empty-membership-points | empty | true | true | true |  |
| empty-invoice-tax-policy | empty | true | true | true |  |
| empty-membership-tier-recovery | empty | true | true | true |  |
| empty-coupon-approval | empty | true | true | true |  |
| empty-password-reset-email | empty | true | true | true |  |
| empty-finance-reconciliation | empty | true | true | true |  |

### token-window-v1

| Case | Category | Hit@K | Citation Match | Empty Handling | Returned Citations |
| --- | --- | --- | --- | --- | --- |
| refund-delayed-shipping | policy | true | false |  | refund_policy_2026#token-window-candidate-1, refund_policy_2026#token-window-2 |
| logistics-delay | faq | true | false |  | logistics_faq_2026#token-window-candidate-1 |
| empty-moon-warehouse | empty | true | true | true |  |
| refund-delivery-paraphrase | paraphrase | true | false |  | refund_policy_2026#token-window-candidate-1 |
| refund-evidence-records | evidence | false | false |  |  |
| logistics-carrier-paraphrase | paraphrase | true | false |  | logistics_faq_2026#token-window-candidate-1 |
| multi-source-after-sales | multi-source | false | false |  |  |
| refund-customized-exception | exception-policy | false | false |  |  |
| refund-high-value-review | operational-escalation | true | false |  | refund_policy_2026#token-window-2 |
| refund-address-change-before-shipping | multi-intent | false | false |  | logistics_faq_2026#token-window-2 |
| logistics-same-city-timeout | sla | true | false |  | logistics_faq_2026#token-window-candidate-1 |
| logistics-lost-package-cross-team | cross-source | true | false |  | logistics_faq_2026#token-window-3 |
| logistics-address-intercept | operational-escalation | true | false |  | logistics_faq_2026#token-window-2 |
| refund-appeal-second-review | long-section | true | false |  | refund_policy_2026#token-window-3, refund_policy_2026#token-window-2 |
| logistics-batch-exception-escalation | long-section | false | false |  |  |
| empty-membership-points | empty | true | true | true |  |
| empty-invoice-tax-policy | empty | true | true | true |  |
| empty-membership-tier-recovery | empty | true | true | true |  |
| empty-coupon-approval | empty | true | true | true |  |
| empty-password-reset-email | empty | true | true | true |  |
| empty-finance-reconciliation | empty | true | true | true |  |
