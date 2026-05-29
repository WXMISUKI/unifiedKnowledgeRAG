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
| created_at | 2026-05-29T06:43:46.189674+00:00 |
| embedding_local_files_only | true |
| embedding_model | BAAI/bge-m3 |
| embedding_model_path | models\bge-m3 |
| embedding_provider | bge_m3_local |
| empty_cases_path | tests\fixtures\hybrid_gating_empty_expanded_cases.json |
| exact_cases_path | tests\fixtures\hybrid_gating_positive_cases.json |
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
| logistics_faq | hybrid_smoke_46b9616da0204583a93699a9872e9be8 | 6 | ready |
| refund_policy_docs | hybrid_smoke_9b631af8530049b4b1684bddb930f40d | 7 | ready |

## Gated Summary

| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |
| --- | ---: | ---: | ---: | ---: |
| qdrant-hybrid:exact-identifier-containment-gate-v1 | 7 | 1.0000 | 1.0000 | 1.0000 |

## Raw And Gated Case Results

| Case | Category | Identifiers | Gate Applied | Raw Citations | Gated Citations | Empty Handling |
| --- | --- | --- | --- | --- | --- | --- |
| hybrid-gating-positive-refund-multi-id | hybrid-gating-multi-id | af-refund-02, rfd-2026-003 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 | refund_policy_2026#exact-refund-code |  |
| hybrid-gating-positive-logistics-multi-id | hybrid-gating-multi-id | lst-batch-ops, ord-zs-2026-0007 | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay | logistics_faq_2026#exact-logistics-id |  |
| hybrid-gating-positive-refund-contextual-id | hybrid-gating-contextual-id | rfd-2026-003 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 | refund_policy_2026#exact-refund-code |  |
| hybrid-gating-empty-partial-refund-form | hybrid-gating-partial-id | af-refund | true | refund_policy_2026#exact-refund-code, refund_policy_2026#high-value-review |  | true |
| hybrid-gating-empty-partial-refund-policy | hybrid-gating-partial-id | rfd-2026 | true | refund_policy_2026#exact-refund-code, refund_policy_2026#section-5 |  | true |
| hybrid-gating-empty-partial-logistics-workflow | hybrid-gating-partial-id | lst-batch | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#delay |  | true |
| hybrid-gating-empty-same-prefix-order | hybrid-gating-same-prefix-id | ord-zs-2026-0008 | true | logistics_faq_2026#exact-logistics-id, logistics_faq_2026#address-intercept |  | true |