# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-hybrid-exact-term-smoke | qdrant | Evaluation-only Qdrant+BGE-M3 dense+sparse smoke path for exact terms, identifiers, acronyms, and order-like ids. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_cases_path | tests\fixtures\exact_term_identifier_cases.json |
| benchmark_fixture | exact-term-identifier-v1 |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-29T04:49:46.308484+00:00 |
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
| logistics_faq | hybrid_smoke_5a3797cfc659453dbcd69d31a712e45b | 6 | ready |
| refund_policy_docs | hybrid_smoke_c419bebc6ac048dfbcafc9f5c0747f6b | 7 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid | 4 | 1.0000 | 1.0000 | 0.0000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| form-name | 1 | 1.0000 | 1.0000 | 0.0000 |
| order-like-id | 1 | 1.0000 | 1.0000 | 0.0000 |
| policy-code | 1 | 1.0000 | 1.0000 | 0.0000 |
| workflow-acronym | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| exact-refund-policy-code | policy-code | medium | true | true |  | 378.091 | refund_policy_2026#exact-refund-code, refund_policy_2026#high-value-review |
| exact-refund-form-name | form-name | medium | true | true |  | 358.003 | refund_policy_2026#exact-refund-code, refund_policy_2026#appeal-review |
| exact-logistics-workflow-acronym | workflow-acronym | hard | true | true |  | 335.230 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay |
| exact-logistics-order-id | order-like-id | hard | true | true |  | 308.962 | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay |
