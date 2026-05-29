# Qdrant BGE-M3 Hybrid Gating Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-hybrid-exact-identifier-gate | qdrant | Evaluation-only Qdrant+BGE-M3 dense+sparse candidate with an exact identifier containment gate for retrieved evidence. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_fixture | hybrid-gating-combined-v1 |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-29T07:26:05.448391+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| empty_cases_path | tests\fixtures\no_benchmark_cases.json |
| exact_cases_path | tests\fixtures\split_chunk_identifier_cases.json |
| fusion | rrf |
| gating_policy | exact-identifier-containment-gate-v1 |
| qdrant_collection | knowledge_chunks |
| qdrant_url | :memory: |
| qdrant_vector_name | text-dense |
| qdrant_vector_size | 1024 |
| rag_score_threshold | 0.7 |
| retrieval_mode | dense+sparse-hybrid |
| score_filter | disabled-for-rrf-fusion-score |
| source_ids | split_refund_policy_docs |
| sparse_vector_name | text-sparse |
| sparse_vectorizer | lexical-identifier-sparse-v1 |

## Indexed Sources

| Source | Job ID | Chunk Count | Status |
| --- | --- | ---: | --- |
| split_refund_policy_docs | hybrid_smoke_0f59bfe2c305499a92050bb8c08410b5 | 2 | ready |

## Gated Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid:exact-identifier-containment-gate-v1 | 1 | 0.0000 | 0.0000 | 0.0000 |

## Raw And Gated Case Results

| Case | Category | Identifiers | Gate Applied | Raw Citations | Gated Citations | Empty Handling |
| --- | --- | --- | --- | --- | --- | --- |
| split-chunk-refund-policy-and-form | split-chunk-identifier | af-refund-02, rfd-2026-003 | true | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code |  |  |