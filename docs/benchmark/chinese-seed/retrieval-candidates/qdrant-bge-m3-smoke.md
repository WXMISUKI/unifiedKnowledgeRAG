# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-smoke | qdrant | Local Qdrant ingestion/retrieval smoke path using the configured embedding adapter, intended for BGE-M3 local evidence. |

## Metadata

| Key | Value |
| --- | --- |
| created_at | 2026-05-28T13:12:17.829693+00:00 |
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
| logistics_faq | smoke_68cb999ccb6b4f67a0cd6dabe3cab2a5 | 4 | ready |
| refund_policy_docs | smoke_dc70260f02c942389ae05191beb0aaef | 5 | ready |

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
| refund-delayed-shipping | policy | easy | true | true |  | 238.076 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| logistics-delay | faq | easy | true | true |  | 240.356 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| empty-moon-warehouse | empty | easy | true | true | true | 208.806 |  |
| refund-delivery-paraphrase | paraphrase | medium | true | true |  | 246.127 | refund_policy_2026#section-3, refund_policy_2026#address-change |
| refund-evidence-records | evidence | easy | true | true |  | 239.820 | refund_policy_2026#section-5, refund_policy_2026#high-value-review |
| logistics-carrier-paraphrase | paraphrase | medium | true | true |  | 239.333 | logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| multi-source-after-sales | multi-source | medium | true | true |  | 289.264 | refund_policy_2026#section-5, refund_policy_2026#address-change, refund_policy_2026#high-value-review |
| refund-customized-exception | exception-policy | medium | true | true |  | 261.498 | refund_policy_2026#exception, refund_policy_2026#high-value-review |
| refund-high-value-review | operational-escalation | medium | true | true |  | 290.072 | refund_policy_2026#high-value-review, refund_policy_2026#section-5 |
| refund-address-change-before-shipping | multi-intent | hard | true | true |  | 399.767 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#section-3 |
| logistics-same-city-timeout | sla | medium | true | true |  | 357.414 | logistics_faq_2026#same-city-timeout, logistics_faq_2026#delay |
| logistics-lost-package-cross-team | cross-source | hard | true | true |  | 406.740 | logistics_faq_2026#lost-package, logistics_faq_2026#delay, logistics_faq_2026#same-city-timeout |
| logistics-address-intercept | operational-escalation | medium | true | true |  | 346.113 | logistics_faq_2026#address-intercept, logistics_faq_2026#delay |
| empty-membership-points | empty | medium | false | false | false | 297.784 | refund_policy_2026#address-change, logistics_faq_2026#address-intercept, refund_policy_2026#high-value-review |
| empty-invoice-tax-policy | empty | hard | true | true | true | 307.819 |  |
