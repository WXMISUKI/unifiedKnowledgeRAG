## ADDED Requirements

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
