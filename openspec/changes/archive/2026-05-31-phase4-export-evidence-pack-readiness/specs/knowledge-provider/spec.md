## ADDED Requirements

### Requirement: Provider handoff includes compact Phase 4 evidence pack readiness export evidence

The system SHALL include optional Phase 4 evidence pack readiness export evidence in provider handoff so reviewers can inspect the current evidence-pack contract coverage without opening the export files separately.

#### Scenario: Handoff summarizes readiness export

- **WHEN** provider handoff reads the Phase 4 readiness export
- **THEN** it summarizes the report status, decision, and contract coverage in a compact row

#### Scenario: Missing readiness export remains non-blocking

- **WHEN** the optional Phase 4 readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior
