## ADDED Requirements

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
