# Qdrant BGE-M3 Hybrid Gating Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-hybrid-multi-chunk-aggregation | qdrant | Evaluation-only Qdrant+BGE-M3 dense+sparse candidate that groups retrieved chunks by source document before checking identifier coverage. |

## Metadata

| Key | Value |
| --- | --- |
| aggregation_policy | source-document-identifier-coverage-v1 |
| benchmark_fixture | split-chunk-identifier-v1 |
| cases_path | tests\fixtures\split_chunk_identifier_cases.json |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-30T05:32:14.211440+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| empty_cases_path | tests\fixtures\multi_chunk_aggregation_negative_cases.json |
| fusion | rrf |
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
| split_refund_policy_docs | hybrid_smoke_b7e58247223048d2bd94656c4181627a | 2 | ready |

## Gated Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid:source-document-identifier-coverage-v1 | 2 | 0.5000 | 0.5000 | 0.0000 |

## Raw And Gated Case Results

| Case | Category | Identifiers | Gate Applied | Raw Citations | Gated Citations | Empty Handling |
| --- | --- | --- | --- | --- | --- | --- |
| split-chunk-refund-policy-and-form | split-chunk-identifier | af-refund-02, rfd-2026-003 | true | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code |  |
| multi-chunk-empty-unsupported-form-policy-link | multi-chunk-aggregation-empty | af-refund-02, rfd-2026-003 | true | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code | split_refund_policy_2026#form-code, split_refund_policy_2026#policy-code | false |