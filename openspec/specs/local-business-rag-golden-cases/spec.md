# local-business-rag-golden-cases Specification

## Purpose
Defines reusable local business RAG golden cases and chunk-quality baseline evidence for approved local business corpora.
## Requirements
### Requirement: Local business golden cases are reusable
The system SHALL maintain a local business RAG golden-case baseline for approved local business corpora without changing runtime retrieval defaults.

#### Scenario: Golden case fixture defines answer expectations
- **WHEN** the local business RAG golden-case baseline is exported
- **THEN** the exported report includes stable case ids, queries, expected modes, expected source ids, expected citation prefixes, and business question types

#### Scenario: Answerable cases require cited evidence
- **WHEN** an answerable golden case is evaluated
- **THEN** the report records whether the provider returned answerable evidence from the expected source and citation prefix

#### Scenario: Expected-empty cases fail closed
- **WHEN** an expected-empty golden case is evaluated
- **THEN** the report records whether the provider returned insufficient evidence without endorsed citations

### Requirement: Chunk quality diagnostics are exported
The system SHALL export chunk-quality diagnostics for the same approved local business corpus used by the golden cases.

#### Scenario: Chunk quality summary is available
- **WHEN** the local business RAG golden-case baseline is exported
- **THEN** the report includes total chunk count, tiny chunk count and ratio, noisy chunk samples, citation anchor count, citation coverage ratio, page coverage, and retrieval case outcomes

#### Scenario: Missing artifacts block the report
- **WHEN** required source, chunk, or case artifacts are missing or invalid
- **THEN** the report decision is `blocked` and the report includes recommended operator actions

#### Scenario: Quality concerns require review
- **WHEN** answerable cases miss expected evidence, expected-empty cases return citations, or chunk-quality thresholds are not satisfied
- **THEN** the report decision is `review` and the report includes the failing reasons

#### Scenario: Passing baseline remains evidence-only
- **WHEN** all golden cases pass and chunk-quality diagnostics meet the local thresholds
- **THEN** the report decision is `go`
- **AND** runtime retrieval defaults, public HTTP APIs, parser ownership, source bindings, vector backends, rerankers, hybrid retrieval, and GraphRAG execution remain unchanged

### Requirement: Real business cases can span multiple sources
The system SHALL support a local aggregate golden-case baseline that can evaluate real business cases across one or more approved local sources.

#### Scenario: Multi-source fixture groups cases by source
- **WHEN** the aggregate local business RAG golden-case baseline is exported
- **THEN** the input fixture can contain cases with `source_id`, `case_id`, `query`, `expected_mode`, `expected_citation_prefix`, `business_question_type`, `failure_mode`, and `risk_level`

#### Scenario: Existing single-source baseline remains compatible
- **WHEN** the aggregate baseline is exported with only `company_profile_2025_trial` cases
- **THEN** it preserves the existing single-source golden-case expectations while adding aggregate source and failure-mode summaries

#### Scenario: Per-source outcomes are visible
- **WHEN** aggregate baseline cases are evaluated
- **THEN** the report includes per-source case counts, hit rate, citation match rate, empty handling rate, invalid citation count, and chunk-quality status

### Requirement: Failure-mode classification guides future work
The system SHALL record failure-mode classification as evidence for future RAG strategy decisions without applying automatic runtime fixes.

#### Scenario: Failure mode summary is exported
- **WHEN** aggregate baseline cases include failure-mode labels
- **THEN** the report summarizes failure-mode counts across parser/OCR, chunking, query mismatch, retrieval quality, citation/evidence, provider availability, caller/operator flow, graph use-case, and unclassified categories

#### Scenario: Failure modes do not change runtime behavior
- **WHEN** a case has a failure-mode label
- **THEN** the provider records the label as review evidence
- **AND** it does not enable query rewrite, rerank, hybrid retrieval, parser ownership changes, MyPrivateAgent orchestration, or GraphRAG execution

#### Scenario: Aggregate result remains conservative
- **WHEN** any source is blocked, any case is blocked, expected-empty cases return citations, answerable cases miss expected evidence, or chunk-quality diagnostics require review
- **THEN** the aggregate report returns `blocked` or `review` rather than `go`

#### Scenario: Passing aggregate baseline remains evidence-only
- **WHEN** all aggregate cases and per-source chunk-quality diagnostics pass
- **THEN** the aggregate report returns `go`
- **AND** runtime retrieval defaults, public HTTP APIs, parser ownership, source bindings, vector backends, rerankers, hybrid retrieval, and GraphRAG execution remain unchanged

### Requirement: Aggregate baseline can carry a second real business source
The system SHALL allow the aggregate local business golden-case baseline to include at least one additional real business source beyond `company_profile_2025_trial` while preserving conservative source-by-source evaluation.

#### Scenario: Second real source is evaluated in the same aggregate report
- **WHEN** the aggregate local business golden-case baseline is exported with cases for `company_profile_2025_trial` and `refund_policy_docs`
- **THEN** the report includes both source ids in `source_reports`
- **AND** the aggregate summary reports `source_count=2`
- **AND** each source is still evaluated through the existing per-source decision and chunk-quality rules

### Requirement: Aggregate multi-source evidence remains strategy-neutral
The system SHALL treat a passing or failing second real business source as evidence for future work selection without changing runtime retrieval behavior automatically.

#### Scenario: Passing second source remains evidence-only
- **WHEN** the aggregate baseline reports `go` after adding a second real business source
- **THEN** the recommended next action continues to be adding more real business documents or real failed questions
- **AND** runtime retrieval defaults, rerank, hybrid retrieval, query rewrite, parser ownership, source binding, and GraphRAG execution remain unchanged

#### Scenario: Failing second source selects only the next evidence gate
- **WHEN** the aggregate baseline reports `review` or `blocked` after adding a second real business source
- **THEN** the report preserves the source-specific failure evidence
- **AND** it does not automatically enable chunking changes, query rewrite, rerank, hybrid retrieval, parser ownership changes, or GraphRAG execution

### Requirement: Aggregate review evidence distinguishes leakage from markdown provenance mismatch
The system SHALL classify real-business aggregate review evidence so callers can distinguish negative-control leakage from markdown provenance/chunk-diagnostic mismatch without changing runtime retrieval behavior.

#### Scenario: Refund-policy review exposes negative-control leakage explicitly
- **WHEN** an aggregate baseline source has expected-empty cases that return evidence or citations
- **THEN** the source report records that review signal as negative-control leakage evidence
- **AND** the aggregate report keeps the source in `review`

#### Scenario: Markdown provenance mismatch stays separate from OCR-like chunk degradation
- **WHEN** a markdown source fails chunk-quality review only because page-level provenance is absent
- **THEN** the source report records a markdown provenance mismatch observation
- **AND** it does not collapse that observation into tiny/noisy chunk degradation

### Requirement: Classified review evidence drives conservative next-step recommendations
The system SHALL use classified review evidence to recommend the next gate without promoting advanced retrieval strategies automatically.

#### Scenario: Leakage review recommends negative-control hardening
- **WHEN** aggregate review evidence includes negative-control leakage
- **THEN** the report recommends reviewing negative-control handling before advanced retrieval strategy changes

#### Scenario: Markdown provenance mismatch recommends diagnostics alignment
- **WHEN** aggregate review evidence includes markdown provenance mismatch
- **THEN** the report recommends reviewing markdown diagnostics or provenance expectations before chunking-default changes
- **AND** runtime retrieval defaults remain unchanged

### Requirement: Chunk diagnostics distinguish paged provenance from markdown provenance
The system SHALL evaluate page coverage only for sources whose chunk or anchor provenance is page-oriented.

#### Scenario: Paged sources still require page coverage
- **WHEN** a local business source exposes page-based chunk provenance such as `#page-1`
- **THEN** chunk-quality diagnostics continue to require page coverage
- **AND** missing page coverage can still contribute to a `review` result

#### Scenario: Non-page markdown sources do not fail page-coverage review by default
- **WHEN** a local business source exposes non-page provenance such as section or exact-term anchors without `#page-*`
- **THEN** chunk-quality diagnostics do not mark the source `review` solely because page ids are absent
- **AND** the report still records the source provenance expectation explicitly

### Requirement: Provenance alignment keeps remaining review causes visible
The system SHALL let remaining real case failures drive review after markdown provenance alignment.

#### Scenario: Markdown provenance alignment isolates negative-control leakage
- **WHEN** a markdown source previously reviewed because of page-coverage mismatch and negative-control leakage
- **THEN** the refreshed report no longer includes the markdown provenance mismatch as a review observation
- **AND** the source can still remain `review` if negative-control leakage persists

### Requirement: Weak lexical overlap does not satisfy negative controls by default
The system SHALL suppress fixture-retriever evidence that only matches weak lexical overlap when real-business local golden cases expect insufficient evidence.

#### Scenario: Weak business-word overlap is filtered for refund-policy negative control
- **WHEN** the fixture retriever evaluates `退款政策里的员工名单有哪些？` against `refund_policy_docs`
- **THEN** weak overlap on generic business terms such as refund/policy wording alone does not produce endorsed evidence
- **AND** the source remains `insufficient_evidence` for that negative control

#### Scenario: Exact-term positive controls remain answerable
- **WHEN** the fixture retriever evaluates exact refund-policy lookups such as `RFD-2026-003 对应哪类退款复核？` or `AF-REFUND-02 表单需要关联哪些付款凭证？`
- **THEN** exact alphanumeric term overlap can still return evidence
- **AND** the existing answerable refund-policy golden cases remain `ready`

#### Scenario: Aggregate baseline returns to go after leakage hardening
- **WHEN** the real-business aggregate baseline is refreshed after negative-control hardening
- **THEN** `refund_policy_docs` no longer records `negative_control_leakage`
- **AND** the aggregate report can return `go` if no other source or chunk-quality review remains

### Requirement: Aggregate real-business baseline can expand to a third approved business source
The system SHALL allow the aggregate local business golden baseline to include a third approved lightweight business source while preserving conservative source-by-source evaluation and runtime-default boundaries.

#### Scenario: Third source appears in aggregate report
- **WHEN** the aggregate local business golden baseline is exported with `company_profile_2025_trial`, `refund_policy_docs`, and `logistics_faq`
- **THEN** the aggregate report includes all three source ids in `source_reports`
- **AND** the summary reports `source_count=3`

#### Scenario: Third source covers new business question types
- **WHEN** `logistics_faq` is added to the aggregate fixture
- **THEN** its cases include at least one workflow/process question, one exact-term identifier question, and one expected-empty negative control
- **AND** those cases continue to use the existing source-specific expected citation behavior

#### Scenario: Breadth expansion remains evidence-only
- **WHEN** the third-source aggregate baseline is refreshed
- **THEN** the result stays `go`, `review`, or `blocked` based on source-specific evidence only
- **AND** it does not automatically enable query rewrite, rerank, hybrid retrieval, chunking-default changes, parser ownership changes, or GraphRAG execution

### Requirement: Real failed-question packs can be exported separately from the passing aggregate baseline
The system SHALL allow a real failed-question pack baseline to reuse the existing aggregate local business evaluation while exporting a separate evidence report for difficult, failed, or boundary questions.

#### Scenario: Failed-question pack writes its own report files
- **WHEN** the real failed-question pack baseline is exported
- **THEN** it writes dedicated JSON and Markdown artifacts separate from `real-business-corpus-golden-cases`
- **AND** it preserves the same conservative `go` / `review` / `blocked` semantics as the aggregate baseline

#### Scenario: Failed-question pack can remain in review while the main aggregate baseline stays go
- **WHEN** the current three-source aggregate baseline is `go` but a failed-question pack includes a real unsupported wording trap
- **THEN** the failed-question pack can return `review`
- **AND** the main aggregate baseline remains an independent breadth signal

### Requirement: Failed-question metadata preserves failure-selection context
The system SHALL preserve minimal metadata that explains why a difficult real-business question belongs in the failed-question pack.

#### Scenario: Failed-question pack records question origin and observed failure
- **WHEN** a failed-question pack fixture is loaded
- **THEN** each case can record `question_origin`, `observed_failure`, and `notes`
- **AND** the exported report summarizes `question_origin`

#### Scenario: Failure metadata remains evidence-only
- **WHEN** a failed-question case is marked as a real failure candidate or cross-domain trap
- **THEN** the provider records that metadata as review evidence only
- **AND** it does not automatically enable query rewrite, rerank, hybrid retrieval, chunk-default changes, parser ownership changes, or GraphRAG execution
