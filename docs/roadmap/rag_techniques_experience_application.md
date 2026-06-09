# RAG Techniques Experience Application

## Purpose

This note translates the local `RAG_Techniques` learning summary into project-specific direction for `unifiedKnowledgeRAG`.

The goal is not to copy notebooks or add advanced RAG techniques by popularity. The goal is to make the provider more mature through failure-mode driven, evidence-backed, lightweight changes.

Reference summary:

`D:\AI\AIcode\经验总结与复用目录\知识库与RAG\RAG_Techniques`

## Core Lessons To Adopt

### RAG is an evaluable pipeline

The mature RAG shape is:

```text
Ingestion -> Chunking -> Indexing -> Query Rewrite -> Retrieval
          -> Rerank/Fusion -> Context Packing -> Generation
          -> Grounding Check -> Evaluation -> Feedback
```

Current project coverage:

| Pipeline Area | Current Status | Next Maturity Need |
| --- | --- | --- |
| Ingestion | Real PDF can be parsed through external PaddleOCR and normalized into parser artifact | Keep parser ownership external; improve acceptance inputs only when real documents expose gaps |
| Chunking | Markdown paragraph/chunk manifest exists; parser-derived chunks are visible | Add chunk quality baseline before changing chunk defaults |
| Indexing | Fixture/in-memory retrieval is usable for local trials | Keep Qdrant/BGE/pgvector candidate-only until quality and operations gates pass |
| Retrieval | Retrieve/answer contracts with citation allowlist and insufficient evidence exist | Evaluate failures by question type before adding query rewrite, hybrid, or rerank |
| Grounding | Evidence pack and citation validation exist | Keep fail-closed negative controls as required gate |
| Evaluation | Local business trial and parser-derived quality baseline exist | Convert real business questions into reusable golden cases |

## Direction For This Project

### Adopt now

1. Golden cases for real business documents
   - Store answerable and insufficient-evidence cases.
   - Track expected source id, expected citation behavior, and business question type.
   - Use them before any retrieval or chunking change.

2. Chunk quality baseline
   - Measure chunk count, tiny/noisy chunk ratio, citation anchor coverage, page/section provenance, and top-k citation stability.
   - Use the current real company-profile PDF as the first local case.
   - Do not change chunking defaults until the baseline shows a real failure pattern.

3. Failure-mode classification
   - Classify each failed trial into parser/OCR, chunking, query mismatch, retrieval quality, citation/evidence, provider availability, or caller/operator flow.
   - Pick the next change from the failure class, not from a generic roadmap phase number.

4. Evidence-first retrieval quality review
   - Keep hit rate, citation match, no-answer accuracy, invalid citation count, latency, and source coverage visible.
   - Compare pipeline changes against the same golden cases.

### Adopt only when triggered

| Technique | Trigger Condition | Why Not Now |
| --- | --- | --- |
| Query rewrite / step-back / sub-query | Real questions miss evidence because user wording and document wording differ | Current real trial answers core company-profile questions |
| HyDE | Short or vague user queries repeatedly fail retrieval while documents contain evidence | Adds query-time LLM cost and audit complexity |
| HyPE / document augmentation | Stable corpus needs better query matching and indexing-side cost is acceptable | Adds index-side generated text and storage complexity |
| Rerank | Recall is enough but top-k precision is noisy | Current trial has citation-valid answers; no rerank failure yet |
| Fusion / hybrid retrieval | Keyword and semantic retrieval each solve different observed cases | Current default is still lightweight fixture/in-memory; promotion gates remain open |
| Context compression / segment extraction | Retrieved chunks are too long or context packing causes answer drift | Current provider answer is deterministic and citation-limited |
| RAPTOR / hierarchical indices | Long documents need multi-level summaries and single-layer chunks fail | No long-document summary failure has been accepted yet |
| Self-RAG / CRAG | Need automated retrieval sufficiency correction with controlled loop limits | Adds judge/correction cost and control-flow complexity |
| GraphRAG | Relationship-heavy, entity/path/multi-hop questions become real requirements | Current company-profile questions are document RAG cases |

### Do not adopt by default

- Do not replace the provider with notebook code.
- Do not promote Qdrant, pgvector, BGE, hybrid search, rerank, GraphRAG, or RAPTOR by popularity.
- Do not put parser engines directly inside the provider unless real corpus demand justifies the ownership cost.
- Do not make generated/rewritten context the final citation; citations must point back to source chunks/pages.
- Do not let query rewrite silently change user intent.

## Recommended Next Stage

Next stage is now implemented:

```text
Local Business RAG Golden Cases And Chunk Quality Baseline
```

Primary repository:

`unifiedKnowledgeRAG`

Why:

- The local real-PDF trial now returns `go`.
- The next maturity gap is not access or provider evidence; it is repeatable quality measurement.
- Chunk quality is the first likely improvement area because OCR-derived PDF text can produce many short/noisy chunks even when the current trial passes.

Completion signal:

- A reusable golden-case fixture/report exists for the current company-profile trial:
  `docs/local-run/business-rag-golden-cases/local-business-rag-golden-cases.json`
- The report includes 4 answerable cases and 2 negative-control cases.
- The same report includes chunk-quality diagnostics: `total_chunk_count=1005`, `tiny_chunk_count=412`, `tiny_chunk_ratio=0.41`, `citation_coverage_ratio=1.0`, and `page_coverage_count=10`.
- The report returns `decision=go`, with `hit_rate=1.0`, `citation_match_rate=1.0`, `empty_handling_rate=1.0`, and `invalid_citation_count=0`.
- Runtime defaults remain unchanged.
- An aggregate real-business corpus fixture/report now also exists:
  `docs/local-run/business-rag-golden-cases/real-business-corpus-golden-cases.json`
- The aggregate report now has `source_count=3` and `case_count=12`, and it remains `go`.
- The third real source `logistics_faq` adds workflow/process, exact-identifier, and negative-control coverage while keeping `hit_rate=1.0`, `citation_match_rate=1.0`, and `empty_handling_rate=1.0`.
- A separate failed-question pack report now also exists at `docs/local-run/business-rag-golden-cases/real-failed-question-pack.json`, and it returns `review` on a real organization-question trap against `refund_policy_docs`.
- A refund-specific confirmation report now also exists at `docs/local-run/business-rag-golden-cases/refund-organization-negative-control-confirmation.json`.
- That confirmation report currently returns `review` with `likely_failure_class=confirmed_negative_control_variant`, `expected_empty_review_count=2`, and `answerable_pass_count=3`.
- A unified source evaluation pack catalog now also exists at `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.json`.
- A source evaluation pack onboarding scaffold now also exists at `docs/local-run/business-rag-golden-cases/onboarding/source_template_example/source-evaluation-pack-onboarding.json`.
- A real-source onboarding validation now also exists for `split_refund_policy_docs` at `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/split-refund-local-business-rag-golden-cases.json`, and it returns `go`.
- A second real-source onboarding validation now also exists for `invoice_policy_faq` at `docs/local-run/business-rag-golden-cases/onboarding/invoice_policy_faq/invoice-policy-local-business-rag-golden-cases.json`, and it returns `go`.
- This means the project now has a passing breadth baseline, a failure-focused review baseline, a smaller confirmation baseline, a provider-level catalog view, a standardized onboarding scaffold, and multiple real-source proofs that the template path works across different source shapes. The next step is to extend provider-general onboarding/discovery usability, not advanced RAG strategy promotion.

Non-goals:

- No GraphRAG.
- No rerank/hybrid/vector backend promotion.
- No source binding.
- No MyPrivateAgent orchestration.
- No parser engine adoption inside the provider.

## Suggested Task Breakdown

### Specification

- Create an OpenSpec change, suggested id:
  `add-local-business-rag-golden-cases-and-chunk-quality-baseline`
- Define golden case schema:
  - `case_id`
  - `query`
  - `expected_mode`
  - `expected_source_id`
  - `expected_citation_prefix`
  - `business_question_type`
- Define chunk quality outputs:
  - total chunks
  - tiny chunk count/ratio
  - citation anchor count
  - page coverage
  - noisy sample snippets
  - retrieval decision
- Declare non-goals clearly.

### Implementation

- Add a small fixture or generated case file for `company_profile_2025_trial`.
- Add an exporter script that reads the approved local source manifest/chunk manifest and runs the golden cases.
- Reuse existing retrieve/answer/evidence-pack contracts.
- Produce JSON and Markdown under:
  `docs/local-run/business-rag-golden-cases/`

### Verification

- Add focused tests for:
  - all cases pass -> `go`
  - answerable case misses evidence -> `review`
  - negative control returns citations -> `review`
  - missing source/chunk artifact -> `blocked`
- Run focused pytest and strict OpenSpec validation.

### Archive

- Archive the change.
- Update this roadmap note and provider tracker with the final verdict.

## Decision Rule For Future Work

After the golden/chunk baseline:

| Baseline Result | Next Direction |
| --- | --- |
| `go` with acceptable chunk quality | Continue testing more real documents; no feature change |
| Answerable misses evidence | Consider query rewrite or chunk strategy evaluation |
| Negative control leaks citations | Strengthen insufficient-evidence guard or citation validation |
| Many tiny/noisy chunks | Evaluate chunk merging, contextual headers, or proposition chunking |
| Top-k has relevant source but poor ordering | Consider rerank candidate review |
| Relationship-heavy questions fail | Open GraphRAG use-case gate |
