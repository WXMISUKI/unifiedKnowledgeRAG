## ADDED Requirements

### Requirement: Provider handoff includes compact Phase 5 graph boundary smoke summary evidence

The system SHALL include optional Phase 5 graph boundary smoke summary evidence in provider handoff so reviewers can inspect the current GraphRAG boundary without opening the full provider contract smoke report separately.

#### Scenario: Handoff summarizes graph boundary smoke

- **WHEN** provider handoff reads the Phase 5 graph boundary smoke summary
- **THEN** it summarizes graph schema discovery, the planned graph query boundary, and the compact graph boundary evidence in one row

#### Scenario: Missing graph boundary smoke summary remains non-blocking

- **WHEN** the optional Phase 5 graph boundary smoke summary is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior
