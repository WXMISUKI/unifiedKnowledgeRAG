# Qdrant BGE-M3 Threshold Sweep Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-smoke | qdrant | Local Qdrant ingestion/retrieval smoke path using the configured embedding adapter, intended for BGE-M3 local evidence. |

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T13:12:58.774878+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| qdrant_collection | knowledge_chunks |
| qdrant_url | :memory: |
| qdrant_vector_name | text-dense |
| qdrant_vector_size | 1024 |
| rag_score_threshold | sweep |
| source_ids | refund_policy_docs, logistics_faq |
| thresholds | 0.3, 0.5, 0.7 |

## Threshold Summary

| Threshold | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| ---: | ---: | ---: | ---: | ---: |
| 0.3000 | 15 | 0.8000 | 0.8000 | 0.0000 |
| 0.5000 | 15 | 0.9333 | 0.9333 | 0.6667 |
| 0.7000 | 15 | 1.0000 | 1.0000 | 1.0000 |

## Case Results By Threshold

### Threshold 0.3000

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Returned Citations |
| --- | --- | --- | --- | --- | --- | --- |
| refund-delayed-shipping | policy | easy | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | false | false | false | refund_policy_2026#exception, refund_policy_2026#address-change, refund_policy_2026#section-5 |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | refund_policy_2026#section-5, refund_policy_2026#address-change, refund_policy_2026#high-value-review |
| refund-customized-exception | exception-policy | medium | true | true |  | refund_policy_2026#exception, refund_policy_2026#high-value-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | refund_policy_2026#high-value-review, refund_policy_2026#section-5 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | logistics_faq_2026#lost-package, logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| logistics-address-intercept | operational-escalation | medium | true | true |  | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | false | false | false | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#high-value-review |
| empty-invoice-tax-policy | empty | hard | false | false | false | refund_policy_2026#section-5, refund_policy_2026#high-value-review, logistics_faq_2026#lost-package |

### Threshold 0.5000

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Returned Citations |
| --- | --- | --- | --- | --- | --- | --- |
| refund-delayed-shipping | policy | easy | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | true | true | true |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | refund_policy_2026#section-5, refund_policy_2026#address-change, refund_policy_2026#high-value-review |
| refund-customized-exception | exception-policy | medium | true | true |  | refund_policy_2026#exception, refund_policy_2026#high-value-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | refund_policy_2026#high-value-review, refund_policy_2026#section-5 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | logistics_faq_2026#lost-package, logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| logistics-address-intercept | operational-escalation | medium | true | true |  | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | false | false | false | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#high-value-review |
| empty-invoice-tax-policy | empty | hard | true | true | true |  |

### Threshold 0.7000

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Returned Citations |
| --- | --- | --- | --- | --- | --- | --- |
| refund-delayed-shipping | policy | easy | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | logistics_faq_2026#delay |
| empty-moon-warehouse | empty | easy | true | true | true |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | refund_policy_2026#section-5, refund_policy_2026#address-change |
| refund-customized-exception | exception-policy | medium | true | true |  | refund_policy_2026#exception |
| refund-high-value-review | operational-escalation | medium | true | true |  | refund_policy_2026#high-value-review |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | logistics_faq_2026#lost-package |
| logistics-address-intercept | operational-escalation | medium | true | true |  | logistics_faq_2026#address-intercept |
| empty-membership-points | empty | medium | true | true | true |  |
| empty-invoice-tax-policy | empty | hard | true | true | true |  |
