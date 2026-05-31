## ADDED Requirements

### Requirement: Provider handoff includes compact Phase 3 readiness export evidence

The system SHALL include optional Phase 3 retrieval promotion readiness evidence in provider handoff so reviewers can inspect the current promotion gap picture without opening the export files separately.

#### Scenario: Handoff summarizes readiness export

- **WHEN** provider handoff reads the Phase 3 readiness export
- **THEN** it summarizes the report status, decision, and open gates in a compact row

#### Scenario: Missing readiness export remains non-blocking

- **WHEN** the optional Phase 3 readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior
