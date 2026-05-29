# Qdrant BGE-M3 Hybrid Gating Evidence

## Candidate

| ID | Backend | Description |
| --- | --- | --- |
| qdrant-bge-m3-hybrid-exact-identifier-gate | qdrant | Evaluation-only Qdrant+BGE-M3 dense+sparse candidate with an exact identifier containment gate for retrieved evidence. |

## Metadata

| Key | Value |
| --- | --- |
| benchmark_fixture | exact-term-identifier-v1+hybrid-empty-stress-v1 |
| chunking_strategy | markdown-paragraph-v1 |
| created_at | 2026-05-29T06:32:57.440806+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| empty_cases_path | tests\fixtures\hybrid_empty_stress_cases.json |
| exact_cases_path | tests\fixtures\exact_term_identifier_cases.json |
| fusion | rrf |
| gating_policy | exact-identifier-containment-gate-v1 |
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
| logistics_faq | hybrid_smoke_35baf94dbab7487aac79bf5ee57d56ba | 6 | ready |
| refund_policy_docs | hybrid_smoke_5b589fbd42824ffb97e01e08b32de7a4 | 7 | ready |

## Gated Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid:exact-identifier-containment-gate-v1 | 8 | 1.0000 | 1.0000 | 1.0000 |

## Raw And Gated Case Results

| Case | Category | Identifiers | Gate Applied | Raw Citations | Gated Citations | Empty Handling |
| --- | --- | --- | --- | --- | --- | --- |
| exact-refund-policy-code | policy-code | rfd-2026-003 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#high-value-review | refund_policy_2026#exact-refund-code |  |
| exact-refund-form-name | form-name | af-refund-02 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#appeal-review | refund_policy_2026#exact-refund-code |  |
| exact-logistics-workflow-acronym | workflow-acronym | lst-batch-ops | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay | logistics_faq_2026#exact-logistics-id |  |
| exact-logistics-order-id | order-like-id | ord-zs-2026-0007 | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay | logistics_faq_2026#exact-logistics-id |  |
| hybrid-empty-fake-refund-form | hybrid-empty-form-name | af-refund-99 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |  | true |
| hybrid-empty-fake-refund-policy-code | hybrid-empty-policy-code | rfd-2026-999 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |  | true |
| hybrid-empty-fake-logistics-workflow | hybrid-empty-workflow-acronym | lst-batch-billing | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay |  | true |
| hybrid-empty-fake-order-id | hybrid-empty-order-like-id | ord-zs-2026-9999 | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#address-intercept |  | true |