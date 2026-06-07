# Local Business Corpus Trial

- Report: `local-business-corpus-trial-loop-v1`
- Decision: `go`
- Reason: `local_business_corpus_usable`
- Generated At: `2026-06-07T09:19:19.698465+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Markdown Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\parser-artifact-local-ingestion-loop\normalized-parser-artifact-boundary\parser-derived-source.md`
- Query: `公司主营业务是什么？`

## Summary

| Metric | Value |
|---|---|
| `decision` | `go` |
| `source_id` | `company_profile_2025_trial` |
| `markdown_char_count` | `464` |
| `chunk_count` | `5` |
| `retrieved_evidence_count` | `2` |
| `answer_citation_count` | `2` |
| `invalid_citation_count` | `0` |
| `trial_overlay_status` | `written` |
| `formal_registration_status` | `not_registered` |
| `default_source_catalog_status` | `unchanged` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Overlay

- Overlay Path: `docs\local-run\parser-artifact-local-ingestion-loop\approved-source-ingestion-loop\document-source-onboarding\business-corpus-trial\local-business-corpus-source.json`
- Owner: `local_trial`
- Domain: `company_profile`
- Sensitivity: `local_private_trial`
- Formal Registration: `not_registered`

## Retrieved Evidence

| Citation | Score | Preview |
|---|---:|---|
| `company_profile_2025_trial#chunk-3` | `0.6667` | 公司简介资料前五页包含公司基本情况、主营业务、服务范围和资质能力说明，可作为本地企业知识库试用语料。 |
| `company_profile_2025_trial#chunk-5` | `0.6667` | 公司业务信息适合用于回答企业介绍、主营业务、服务对象和资质能力类问题，后续可通过正式解析器刷新更完整文本。 |

## Trial Answer

公司简介资料前五页包含公司基本情况、主营业务、服务范围和资质能力说明，可作为本地企业知识库试用语料；公司业务信息适合用于回答企业介绍、主营业务、服务对象和资质能力类问题，后续可通过正式解析器刷新更完整文本。引用：[company_profile_2025_trial#chunk-3] [company_profile_2025_trial#chunk-5]

## Recommended Actions

- review_local_business_corpus_quality_before_formal_registration
- use_trial_overlay_as_input_for_future_source_registration_design
- keep_default_source_catalog_unchanged

## Notes

- This is a local business corpus trial, not formal provider source registration.
- The default provider source catalog and HTTP source list remain unchanged.
- The trial does not run formal ingestion jobs, persist index lifecycle state, create source bindings, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration.
