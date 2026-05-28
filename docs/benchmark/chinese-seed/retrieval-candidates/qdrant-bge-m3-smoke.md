# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-smoke | qdrant | Local Qdrant ingestion/retrieval smoke path using the configured embedding adapter, intended for BGE-M3 local evidence. |

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T13:41:12.121852+00:00 |
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
| logistics_faq | smoke_a864be9e50eb4fcb84abbdfa064de4c1 | 5 | ready |
| refund_policy_docs | smoke_74af4740e7be4a0495f4785a5564e36f | 6 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant | 21 | 0.7619 | 0.7619 | 0.2857 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 7 | 0.2857 | 0.2857 | 0.2857 |
| evidence | 1 | 1.0000 | 1.0000 | 0.0000 |
| exception-policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| faq | 1 | 1.0000 | 1.0000 | 0.0000 |
| long-section | 2 | 1.0000 | 1.0000 | 0.0000 |
| multi-intent | 1 | 1.0000 | 1.0000 | 0.0000 |
| multi-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| operational-escalation | 2 | 1.0000 | 1.0000 | 0.0000 |
| paraphrase | 2 | 1.0000 | 1.0000 | 0.0000 |
| policy | 1 | 1.0000 | 1.0000 | 0.0000 |
| sla | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| refund-delayed-shipping | policy | easy | true | true |  | 307.913 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | 312.442 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | true | true | true | 280.153 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 326.529 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | 314.994 | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 312.192 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | 329.483 | refund_policy_2026#section-5, refund_policy_2026#address-change, refund_policy_2026#appeal-review |
| refund-customized-exception | exception-policy | medium | true | true |  | 308.247 | refund_policy_2026#exception, refund_policy_2026#high-value-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 327.468 | refund_policy_2026#high-value-review, refund_policy_2026#section-5 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 358.266 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 338.768 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 344.814 | logistics_faq_2026#lost-package, logistics_faq_2026#batch-exception, logistics_faq_2026#delay |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 332.661 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| refund-appeal-second-review | long-section | hard | true | true |  | 356.424 | refund_policy_2026#appeal-review, refund_policy_2026#address-change, refund_policy_2026#section-5 |
| logistics-batch-exception-escalation | long-section | hard | true | true |  | 370.512 | logistics_faq_2026#batch-exception, logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-membership-points | empty | medium | false | false | false | 309.235 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#high-value-review |
| empty-invoice-tax-policy | empty | hard | true | true | true | 329.784 |  |
| empty-membership-tier-recovery | empty | medium | false | false | false | 306.329 | refund_policy_2026#high-value-review |
| empty-coupon-approval | empty | medium | false | false | false | 324.693 | refund_policy_2026#high-value-review, refund_policy_2026#address-change, refund_policy_2026#section-5 |
| empty-password-reset-email | empty | medium | false | false | false | 310.544 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay, refund_policy_2026#address-change |
| empty-finance-reconciliation | empty | hard | false | false | false | 318.553 | refund_policy_2026#high-value-review, refund_policy_2026#section-5, refund_policy_2026#address-change |
