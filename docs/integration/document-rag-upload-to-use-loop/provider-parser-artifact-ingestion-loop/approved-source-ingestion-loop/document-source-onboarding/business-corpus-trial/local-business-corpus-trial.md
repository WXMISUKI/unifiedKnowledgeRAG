# Local Business Corpus Trial

- Report: `local-business-corpus-trial-loop-v1`
- Decision: `go`
- Reason: `local_business_corpus_usable`
- Generated At: `2026-06-08T01:32:38.283234+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025-10-27`
- Markdown Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\integration\document-rag-upload-to-use-loop\provider-parser-artifact-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md`
- Query: `公司主营业务是什么？`

## Summary

| Metric | Value |
|---|---|
| `decision` | `go` |
| `source_id` | `company_profile_2025_trial` |
| `markdown_char_count` | `44205` |
| `chunk_count` | `678` |
| `retrieved_evidence_count` | `3` |
| `answer_citation_count` | `3` |
| `invalid_citation_count` | `0` |
| `trial_overlay_status` | `written` |
| `formal_registration_status` | `not_registered` |
| `default_source_catalog_status` | `unchanged` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Overlay

- Overlay Path: `docs\integration\document-rag-upload-to-use-loop\provider-parser-artifact-ingestion-loop\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-source.json`
- Owner: `local_trial`
- Domain: `company_profile`
- Sensitivity: `local_private_trial`
- Formal Registration: `not_registered`

## Retrieved Evidence

| Citation | Score | Preview |
|---|---:|---|
| `company_profile_2025_trial#chunk-111` | `0.6667` | “今天的业主是我们永远的业主”为服务宗旨，践行“用诚信和实力塑造公司品牌” |
| `company_profile_2025_trial#chunk-83` | `0.4444` | 公司主要经营高等级公路、大型桥梁和隧道工程及水运工程的施工监理、技术 |
| `company_profile_2025_trial#chunk-87` | `0.3333` | 监理。公司设市场开发部、财务审计部、办公室、中心试验室，现有员工478名， |

## Trial Answer

“今天的业主是我们永远的业主”为服务宗旨，践行“用诚信和实力塑造公司品牌”；公司主要经营高等级公路、大型桥梁和隧道工程及水运工程的施工监理、技术；监理。引用：[company_profile_2025_trial#chunk-111] [company_profile_2025_trial#chunk-83] [company_profile_2025_trial#chunk-87]

## Recommended Actions

- review_local_business_corpus_quality_before_formal_registration
- use_trial_overlay_as_input_for_future_source_registration_design
- keep_default_source_catalog_unchanged

## Notes

- This is a local business corpus trial, not formal provider source registration.
- The default provider source catalog and HTTP source list remain unchanged.
- The trial does not run formal ingestion jobs, persist index lifecycle state, create source bindings, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration.
