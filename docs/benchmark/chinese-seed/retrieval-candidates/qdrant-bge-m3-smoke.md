# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-smoke | qdrant | Local Qdrant ingestion/retrieval smoke path using the configured embedding adapter, intended for BGE-M3 local evidence. |

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T13:19:08.693414+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| qdrant_collection | knowledge_chunks |
| qdrant_url | :memory: |
| qdrant_vector_name | text-dense |
| qdrant_vector_size | 1024 |
| rag_score_threshold | 0.5 |
| source_ids | refund_policy_docs, logistics_faq |

## Indexed Sources

| Source | Job ID | Chunk Count | Status |
| --- | --- | ---: | --- |
| logistics_faq | smoke_63d3380f83d84d34a815e97176ac4c05 | 4 | ready |
| refund_policy_docs | smoke_b5363d9a77824947a1005747cc36c63c | 5 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant | 19 | 0.7368 | 0.7368 | 0.2857 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 7 | 0.2857 | 0.2857 | 0.2857 |
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
| refund-delayed-shipping | policy | easy | true | true |  | 222.605 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | 228.217 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | true | true | true | 220.962 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 244.748 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | 248.046 | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 242.956 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | 267.276 | refund_policy_2026#section-5, refund_policy_2026#address-change, refund_policy_2026#high-value-review |
| refund-customized-exception | exception-policy | medium | true | true |  | 258.229 | refund_policy_2026#exception, refund_policy_2026#high-value-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 251.499 | refund_policy_2026#high-value-review, refund_policy_2026#section-5 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 305.643 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 330.946 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 337.422 | logistics_faq_2026#lost-package, logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 318.106 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | false | false | false | 276.453 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#high-value-review |
| empty-invoice-tax-policy | empty | hard | true | true | true | 294.858 |  |
| empty-membership-tier-recovery | empty | medium | false | false | false | 270.521 | refund_policy_2026#high-value-review |
| empty-coupon-approval | empty | medium | false | false | false | 289.569 | refund_policy_2026#high-value-review, refund_policy_2026#address-change, refund_policy_2026#section-5 |
| empty-password-reset-email | empty | medium | false | false | false | 274.315 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay, refund_policy_2026#address-change |
| empty-finance-reconciliation | empty | hard | false | false | false | 277.655 | refund_policy_2026#high-value-review, refund_policy_2026#section-5, refund_policy_2026#address-change |
