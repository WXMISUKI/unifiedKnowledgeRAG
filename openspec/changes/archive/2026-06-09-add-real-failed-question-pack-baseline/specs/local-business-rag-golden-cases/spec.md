## ADDED Requirements

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
