# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-smoke | qdrant | Local Qdrant ingestion/retrieval smoke path using the configured embedding adapter, intended for BGE-M3 local evidence. |

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T12:27:14.651371+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| qdrant_collection | knowledge_chunks |
| qdrant_url | :memory: |
| qdrant_vector_name | text-dense |
| qdrant_vector_size | 1024 |
| source_ids | refund_policy_docs, logistics_faq |

## Indexed Sources

| Source | Job ID | Chunk Count | Status |
| --- | --- | ---: | --- |
| logistics_faq | smoke_21ecc33cc58e44af91d6405fafb66779 | 4 | ready |
| refund_policy_docs | smoke_0d9f39383a884faab4f1d41c9a0e9986 | 5 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant | 15 | 0.8000 | 0.0000 | 0.0000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| cross-source | 1 | 1.0000 | 0.0000 | 0.0000 |
| empty | 3 | 0.0000 | 0.0000 | 0.0000 |
| evidence | 1 | 1.0000 | 0.0000 | 0.0000 |
| exception-policy | 1 | 1.0000 | 0.0000 | 0.0000 |
| faq | 1 | 1.0000 | 0.0000 | 0.0000 |
| multi-intent | 1 | 1.0000 | 0.0000 | 0.0000 |
| multi-source | 1 | 1.0000 | 0.0000 | 0.0000 |
| operational-escalation | 2 | 1.0000 | 0.0000 | 0.0000 |
| paraphrase | 2 | 1.0000 | 0.0000 | 0.0000 |
| policy | 1 | 1.0000 | 0.0000 | 0.0000 |
| sla | 1 | 1.0000 | 0.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| refund-delayed-shipping | policy | easy | true | false |  | 268.728 | refund_policy_2026#chunk-1, refund_policy_2026#chunk-5 |
| logistics-delay | faq | easy | true | false |  | 282.653 | logistics_faq_2026#chunk-1, logistics_faq_2026#chunk-2 |
| empty-moon-warehouse | empty | easy | false | false | false | 249.497 | refund_policy_2026#chunk-3, refund_policy_2026#chunk-5, refund_policy_2026#chunk-2 |
| refund-delivery-paraphrase | paraphrase | medium | true | false |  | 298.833 | refund_policy_2026#chunk-1, refund_policy_2026#chunk-5 |
| refund-evidence-records | evidence | easy | true | false |  | 292.235 | refund_policy_2026#chunk-2, refund_policy_2026#chunk-4 |
| logistics-carrier-paraphrase | paraphrase | medium | true | false |  | 288.822 | logistics_faq_2026#chunk-1, logistics_faq_2026#chunk-2 |
| multi-source-after-sales | multi-source | medium | true | false |  | 305.333 | refund_policy_2026#chunk-2, refund_policy_2026#chunk-5, refund_policy_2026#chunk-4 |
| refund-customized-exception | exception-policy | medium | true | false |  | 287.952 | refund_policy_2026#chunk-3, refund_policy_2026#chunk-4 |
| refund-high-value-review | operational-escalation | medium | true | false |  | 313.614 | refund_policy_2026#chunk-4, refund_policy_2026#chunk-2 |
| refund-address-change-before-shipping | multi-intent | hard | true | false |  | 330.786 | refund_policy_2026#chunk-5, logistics_faq_2026#chunk-4, refund_policy_2026#chunk-1 |
| logistics-same-city-timeout | sla | medium | true | false |  | 309.578 | logistics_faq_2026#chunk-2, logistics_faq_2026#chunk-1 |
| logistics-lost-package-cross-team | cross-source | hard | true | false |  | 338.737 | logistics_faq_2026#chunk-3, logistics_faq_2026#chunk-1, logistics_faq_2026#chunk-2 |
| logistics-address-intercept | operational-escalation | medium | true | false |  | 309.915 | logistics_faq_2026#chunk-4, logistics_faq_2026#chunk-1 |
| empty-membership-points | empty | medium | false | false | false | 274.389 | refund_policy_2026#chunk-5, logistics_faq_2026#chunk-4, refund_policy_2026#chunk-4 |
| empty-invoice-tax-policy | empty | hard | false | false | false | 292.301 | refund_policy_2026#chunk-2, refund_policy_2026#chunk-4, logistics_faq_2026#chunk-3 |
