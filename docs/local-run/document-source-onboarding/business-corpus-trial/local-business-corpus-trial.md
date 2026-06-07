# Local Business Corpus Trial

- Report: `local-business-corpus-trial-loop-v1`
- Decision: `go`
- Reason: `local_business_corpus_usable`
- Generated At: `2026-06-07T03:41:01.207118+00:00`
- Source ID: `company_profile_2025_trial`
- Title: `公司简介 2025 trial`
- Markdown Path: `D:\AI\AIcode\unifiedKnowledgeRAG\docs\local-run\pdf-derived-corpus\company_profile_2025_trial.md`
- Query: `公司主营业务是什么？`

## Summary

| Metric | Value |
|---|---|
| `decision` | `go` |
| `source_id` | `company_profile_2025_trial` |
| `markdown_char_count` | `2198` |
| `chunk_count` | `4` |
| `retrieved_evidence_count` | `3` |
| `answer_citation_count` | `3` |
| `invalid_citation_count` | `0` |
| `trial_overlay_status` | `written` |
| `formal_registration_status` | `not_registered` |
| `default_source_catalog_status` | `unchanged` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `graph_execution_status` | `not_executed` |

## Overlay

- Overlay Path: `docs\local-run\document-source-onboarding\business-corpus-trial\local-business-corpus-source.json`
- Owner: `local_trial`
- Domain: `company_profile`
- Sensitivity: `local_private_trial`
- Formal Registration: `not_registered`

## Retrieved Evidence

| Citation | Score | Preview |
|---|---:|---|
| `company_profile_2025_trial#chunk-3` | `0.7778` | 一、公 司 简 介 江苏交通工程咨询监理有限公司成立于1993年5月，拥有公路工程监理甲级、 水运工程监理甲级、特殊独立大桥监理专项、特殊独立隧道监理专项、机电工程监 理专项资质、市政公用工程监理乙级、公路工程综合乙级试验检测资质；公司通过 了IS09001质量管理体系认证、IS |
| `company_profile_2025_trial#chunk-4` | `0.6667` | 二、组 织 机 构 公司设立了市场开发部、财务审计部、办公室、中心试验室的二部二室管理构 架，并先后成立了江苏安泰路桥工程检测有限公司、江苏茂森工程咨询监理有限 公司（原名：江苏茂盛工程咨询监理有限公司）两个独资子公司。 公司主要管理人员： 董事长：徐金法，硕士，高级工程师，国家 |
| `company_profile_2025_trial#chunk-1` | `0.4444` | 企业宗旨: 公正、科学、 诚信、自律 服务理念: 廉洁、尽责、精细、 耐劳、分忧 公司精神: 守法公正、诚信履约、 科学管理、创新服 务 |

## Trial Answer

一、公 司 简 介 江苏交通工程咨询监理有限公司成立于1993年5月，拥有公路工程监理甲级、 水运工程监理甲级、特殊独立大桥监理专项、特殊独立隧道监理专项、机电工程监 理专项资质、市政公用工程监理乙级、公路工程综合乙级试验检测资质；公司通过 了IS09001质量管理体系认证、ISO14001环境管理体系认证、GB/T28001职业健康安 全管理体系认证，是江；二、组 织 机 构 公司设立了市场开发部、财务审计部、办公室、中心试验室的二部二室管理构 架，并先后成立了江苏安泰路桥工程检测有限公司、江苏茂森工程咨询监理有限 公司（原名：江苏茂盛工程咨询监理有限公司）两个独资子公司；企业宗旨: 公正、科学、 诚信、自律 服务理念: 廉洁、尽责、精细、 耐劳、分忧 公司精神: 守法公正、诚信履约、 科学管理、创新服 务。引用：[company_profile_2025_trial#chunk-3] [company_profile_2025_trial#chunk-4] [company_profile_2025_trial#chunk-1]

## Recommended Actions

- review_local_business_corpus_quality_before_formal_registration
- use_trial_overlay_as_input_for_future_source_registration_design
- keep_default_source_catalog_unchanged

## Notes

- This is a local business corpus trial, not formal provider source registration.
- The default provider source catalog and HTTP source list remain unchanged.
- The trial does not run formal ingestion jobs, persist index lifecycle state, create source bindings, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration.
