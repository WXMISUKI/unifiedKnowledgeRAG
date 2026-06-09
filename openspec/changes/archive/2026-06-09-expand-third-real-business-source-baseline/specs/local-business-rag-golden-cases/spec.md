## ADDED Requirements

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
