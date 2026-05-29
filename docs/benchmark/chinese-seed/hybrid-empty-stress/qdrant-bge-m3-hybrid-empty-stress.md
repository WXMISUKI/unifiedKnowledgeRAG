# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-hybrid-empty-stress | qdrant | Evaluation-only Qdrant+BGE-M3 dense+sparse smoke path for expected-empty cases with exact-token overlap. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_cases_path | tests\fixtures\hybrid_empty_stress_cases.json |
| benchmark_fixture | hybrid-empty-stress-v1 |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-29T05:03:04.564800+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| fusion | rrf |
| qdrant_collection | knowledge_chunks |
| qdrant_url | :memory: |
| qdrant_vector_name | text-dense |
| qdrant_vector_size | 1024 |
| rag_score_threshold | 0.7 |
| retrieval_mode | dense+sparse-hybrid |
| score_filter | disabled-for-rrf-fusion-score |
| source_ids | refund_policy_docs, logistics_faq |
| sparse_vector_name | text-sparse |
| sparse_vectorizer | lexical-identifier-sparse-v1 |

## Indexed Sources

| Source | Job ID | Chunk Count | Status |
| --- | --- | ---: | --- |
| logistics_faq | hybrid_smoke_005690103684499b9a6f245752bddc86 | 6 | ready |
| refund_policy_docs | hybrid_smoke_80381934374f4a229755e565d627f879 | 7 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid | 4 | 0.0000 | 0.0000 | 0.0000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| hybrid-empty-form-name | 1 | 0.0000 | 0.0000 | 0.0000 |
| hybrid-empty-order-like-id | 1 | 0.0000 | 0.0000 | 0.0000 |
| hybrid-empty-policy-code | 1 | 0.0000 | 0.0000 | 0.0000 |
| hybrid-empty-workflow-acronym | 1 | 0.0000 | 0.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| hybrid-empty-fake-refund-form | hybrid-empty-form-name | hard | false | false | false | 400.879 | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |
| hybrid-empty-fake-refund-policy-code | hybrid-empty-policy-code | hard | false | false | false | 363.385 | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |
| hybrid-empty-fake-logistics-workflow | hybrid-empty-workflow-acronym | hard | false | false | false | 344.679 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay |
| hybrid-empty-fake-order-id | hybrid-empty-order-like-id | hard | false | false | false | 337.514 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#address-intercept |
