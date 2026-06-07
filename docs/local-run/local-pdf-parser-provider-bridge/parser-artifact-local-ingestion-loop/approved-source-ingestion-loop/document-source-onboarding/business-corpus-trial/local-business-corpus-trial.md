# Local Business Corpus Trial

- Report: `local-business-corpus-trial-loop-v1`
- Decision: `go`
- Reason: `local_business_corpus_usable`
- Generated At: `2026-06-07T10:42:04.941544+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Markdown Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md`
- Query: `公司主营业务和服务范围是什么？`

## Summary

| Metric | Value |
|---|---|
| `decision` | `go` |
| `source_id` | `company_profile_2025_trial` |
| `markdown_char_count` | `10317` |
| `chunk_count` | `158` |
| `retrieved_evidence_count` | `3` |
| `answer_citation_count` | `3` |
| `invalid_citation_count` | `0` |
| `trial_overlay_status` | `written` |
| `formal_registration_status` | `not_registered` |
| `default_source_catalog_status` | `unchanged` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Overlay

- Overlay Path: `docs\local-run\local-pdf-parser-provider-bridge\parser-artifact-local-ingestion-loop\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-source.json`
- Owner: `local_trial`
- Domain: `company_profile`
- Sensitivity: `local_private_trial`
- Formal Registration: `not_registered`

## Retrieved Evidence

| Citation | Score | Preview |
|---|---:|---|
| `company_profile_2025_trial#chunk-104` | `0.6429` | “今天的业主是我们永远的业主”为服务宗旨，践行“用诚信和实力塑造公司品牌” |
| `company_profile_2025_trial#chunk-76` | `0.3571` | 公司主要经营高等级公路、大型桥梁和隧道工程及水运工程的施工监理、技术 |
| `company_profile_2025_trial#chunk-100` | `0.3571` | 理念，持续发扬“守法公正、诚信履约、科学管理、创新服务”的公司精神，以诚 |

## Trial Answer

“今天的业主是我们永远的业主”为服务宗旨，践行“用诚信和实力塑造公司品牌”；公司主要经营高等级公路、大型桥梁和隧道工程及水运工程的施工监理、技术；理念，持续发扬“守法公正、诚信履约、科学管理、创新服务”的公司精神，以诚。引用：[company_profile_2025_trial#chunk-104] [company_profile_2025_trial#chunk-76] [company_profile_2025_trial#chunk-100]

## Recommended Actions

- review_local_business_corpus_quality_before_formal_registration
- use_trial_overlay_as_input_for_future_source_registration_design
- keep_default_source_catalog_unchanged

## Notes

- This is a local business corpus trial, not formal provider source registration.
- The default provider source catalog and HTTP source list remain unchanged.
- The trial does not run formal ingestion jobs, persist index lifecycle state, create source bindings, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration.
