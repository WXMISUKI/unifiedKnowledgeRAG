# Qdrant BGE-M3 Hybrid Gating Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-hybrid-alias-identifier-gate | qdrant | Evaluation-only Qdrant+BGE-M3 dense+sparse candidate with OCR and local alias normalization before identifier gating. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_fixture | noisy-identifier-gating-v1 |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-29T06:57:12.129085+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| empty_cases_path | tests\fixtures\noisy_identifier_empty_cases.json |
| fusion | rrf |
| gating_policy | alias-aware-identifier-gate-v1 |
| positive_cases_path | tests\fixtures\noisy_identifier_positive_cases.json |
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
| logistics_faq | hybrid_smoke_4e2538cfbcff419881cfae227c8f68b0 | 6 | ready |
| refund_policy_docs | hybrid_smoke_6e7c00dfaf294b1aa01c1419a1b38193 | 7 | ready |

## Gated Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid:alias-aware-identifier-gate-v1 | 8 | 1.0000 | 1.0000 | 1.0000 |

## Raw And Gated Case Results

| Case | Category | Identifiers | Gate Applied | Raw Citations | Gated Citations | Empty Handling |
| --- | --- | --- | --- | --- | --- | --- |
| noisy-positive-refund-policy-ocr | noisy-identifier-ocr | rfd-2026-003 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#high-value-review | refund_policy_2026#exact-refund-code |  |
| noisy-positive-refund-form-chinese-alias | noisy-identifier-alias | af-refund-02 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 | refund_policy_2026#exact-refund-code |  |
| noisy-positive-logistics-workflow-chinese-alias | noisy-identifier-alias | lst-batch-ops | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception | logistics_faq_2026#exact-logistics-id |  |
| noisy-positive-logistics-order-ocr-spacing | noisy-identifier-ocr | ord-zs-2026-0007 | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay | logistics_faq_2026#exact-logistics-id |  |
| noisy-empty-refund-form-chinese-alias | noisy-identifier-empty-alias | af-refund-99 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |  | true |
| noisy-empty-refund-policy-ocr | noisy-identifier-empty-ocr | rfd-2026-999 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |  | true |
| noisy-empty-logistics-workflow-chinese-alias | noisy-identifier-empty-alias | lst-batch-billing | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#batch-exception |  | true |
| noisy-empty-logistics-order-ocr-spacing | noisy-identifier-empty-ocr | ord-zs-2026-0008 | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#address-intercept |  | true |