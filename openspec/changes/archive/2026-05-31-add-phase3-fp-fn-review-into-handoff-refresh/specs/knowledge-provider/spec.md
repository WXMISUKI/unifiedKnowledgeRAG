## MODIFIED Requirements

### Requirement: Provider handoff includes compact Phase 3 retrieval baseline evidence

The system SHALL include optional Phase 3 retrieval evidence rows in provider handoff so external reviewers can inspect benchmark quality signals without opening multiple files separately.

#### Scenario: Handoff summarizes Phase 3 FP/FN review evidence

- **WHEN** provider handoff reads the local FP/FN review artifact
- **THEN** it summarizes `false_positive_count`, `false_negative_count`, `false_positive_rate`, and `false_negative_rate`

#### Scenario: Missing FP/FN review evidence remains non-blocking

- **WHEN** the optional FP/FN review artifact is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior
