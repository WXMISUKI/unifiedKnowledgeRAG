## ADDED Requirements

### Requirement: Refund organization-question confirmation baseline remains separate from breadth and failure-pack baselines
The system SHALL allow a refund-specific confirmation baseline to reuse the existing local aggregate evaluation while exporting dedicated evidence for organization-question failure-class confirmation.

#### Scenario: Confirmation baseline writes dedicated report files
- **WHEN** the refund organization-question confirmation baseline is exported
- **THEN** it writes dedicated JSON and Markdown artifacts separate from `real-business-corpus-golden-cases` and `real-failed-question-pack`
- **AND** it preserves the same conservative `go` / `review` / `blocked` semantics as the existing aggregate evaluation engine

#### Scenario: Confirmation baseline stays source-specific and strategy-neutral
- **WHEN** the confirmation baseline evaluates only `refund_policy_docs`
- **THEN** it records evidence for the refund source only
- **AND** it does not automatically enable query rewrite, rerank, hybrid retrieval, chunk-default changes, parser ownership changes, or GraphRAG execution

### Requirement: Confirmation baseline classifies likely failure class conservatively
The system SHALL summarize refund organization-question confirmation results into a conservative likely failure class and next gate without applying runtime fixes automatically.

#### Scenario: Negative-control leakage is confirmed when organization negatives review but role positives pass
- **WHEN** organization/department/staff-list expected-empty variants return review evidence while role/responsibility answerable variants pass
- **THEN** the confirmation report sets `likely_failure_class` to `confirmed_negative_control_variant`
- **AND** it recommends a negative-control-focused next gate rather than query rewrite or broader retrieval promotion

#### Scenario: Query mismatch is confirmed when organization negatives fail closed but role positives miss evidence
- **WHEN** organization/department/staff-list expected-empty variants remain fail-closed while role/responsibility answerable variants miss expected evidence
- **THEN** the confirmation report sets `likely_failure_class` to `confirmed_query_mismatch_variant`
- **AND** it recommends a wording/query-mismatch evidence gate rather than automatic runtime strategy changes

#### Scenario: Mixed signals remain review evidence only
- **WHEN** both expected-empty variants and answerable variants review in the same confirmation baseline
- **THEN** the confirmation report sets `likely_failure_class` to `mixed_signal_needs_more_cases`
- **AND** it recommends collecting more focused refund variants before any advanced retrieval strategy candidate is promoted

#### Scenario: No stable pattern does not open a new strategy slice
- **WHEN** the confirmation baseline does not expose a stable review pattern
- **THEN** the confirmation report sets `likely_failure_class` to `not_enough_evidence`
- **AND** runtime retrieval defaults, public HTTP APIs, source bindings, rerankers, hybrid retrieval, and GraphRAG execution remain unchanged
