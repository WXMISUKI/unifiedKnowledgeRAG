# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-smoke | qdrant | Local Qdrant ingestion/retrieval smoke path using the configured embedding adapter, intended for BGE-M3 local evidence. |

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T12:56:52.425995+00:00 |
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
| logistics_faq | smoke_0ad2225a8b9f44fe9cc7b4f694511f85 | 4 | ready |
| refund_policy_docs | smoke_438f033e3b0648bd928d810f2eb052a1 | 5 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant | 15 | 0.9333 | 0.9333 | 0.6667 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 1.0000 | 0.0000 |
| empty | 3 | 0.6667 | 0.6667 | 0.6667 |
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
| refund-delayed-shipping | policy | easy | true | true |  | 265.186 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | 280.127 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | true | true | true | 251.116 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 295.903 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | 294.237 | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 299.145 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | 305.119 | refund_policy_2026#section-5, refund_policy_2026#address-change, refund_policy_2026#high-value-review |
| refund-customized-exception | exception-policy | medium | true | true |  | 290.687 | refund_policy_2026#exception, refund_policy_2026#high-value-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 300.440 | refund_policy_2026#high-value-review, refund_policy_2026#section-5 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 329.421 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 299.427 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 334.555 | logistics_faq_2026#lost-package, logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 324.569 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | false | false | false | 282.612 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#high-value-review |
| empty-invoice-tax-policy | empty | hard | true | true | true | 291.746 |  |
