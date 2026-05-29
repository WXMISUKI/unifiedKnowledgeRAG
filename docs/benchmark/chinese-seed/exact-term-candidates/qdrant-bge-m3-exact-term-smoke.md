# Qdrant BGE-M3 Smoke Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-exact-term-smoke | qdrant | Local Qdrant+BGE-M3 dense-only smoke path for exact terms, identifiers, acronyms, and order-like ids. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_cases_path | tests\fixtures\exact_term_identifier_cases.json |
| benchmark_fixture | exact-term-identifier-v1 |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-29T04:06:10.227725+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| qdrant_collection | knowledge_chunks |
| qdrant_url | :memory: |
| qdrant_vector_name | text-dense |
| qdrant_vector_size | 1024 |
| rag_score_threshold | 0.7 |
| source_ids | refund_policy_docs, logistics_faq |

## Indexed Sources

| Source | Job ID | Chunk Count | Status |
| --- | --- | ---: | --- |
| logistics_faq | smoke_8e9542c9d7054c1a8b9a837dac0bcec5 | 6 | ready |
| refund_policy_docs | smoke_06172ca41f5c4919b534fb65e6ccd21f | 7 | ready |

# Retrieval Benchmark Report

## Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant | 4 | 0.5000 | 0.5000 | 0.0000 |

## Category Summary

| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| form-name | 1 | 0.0000 | 0.0000 | 0.0000 |
| order-like-id | 1 | 0.0000 | 0.0000 | 0.0000 |
| policy-code | 1 | 1.0000 | 1.0000 | 0.0000 |
| workflow-acronym | 1 | 1.0000 | 1.0000 | 0.0000 |

## Case Results

| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| exact-refund-policy-code | policy-code | medium | true | true |  | 334.386 | refund_policy_2026#exact-refund-code |
| exact-refund-form-name | form-name | medium | false | false |  | 318.839 |  |
| exact-logistics-workflow-acronym | workflow-acronym | hard | true | true |  | 308.600 | logistics_faq_2026#exact-logistics-id |
| exact-logistics-order-id | order-like-id | hard | false | false |  | 309.227 |  |
