## ADDED Requirements

### Requirement: Provider handoff includes compact Phase 5 graph use-case readiness export evidence

The system SHALL include optional Phase 5 graph use-case readiness export evidence in provider handoff so reviewers can inspect the current GraphRAG boundary without opening the export files separately.

#### Scenario: Handoff summarizes graph readiness export

- **WHEN** provider handoff reads the Phase 5 graph readiness export
- **THEN** it summarizes the report status, decision, and graph boundary evidence in a compact row

#### Scenario: Missing graph readiness export remains non-blocking

- **WHEN** the optional Phase 5 graph readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior
