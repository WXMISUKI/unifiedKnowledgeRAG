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

