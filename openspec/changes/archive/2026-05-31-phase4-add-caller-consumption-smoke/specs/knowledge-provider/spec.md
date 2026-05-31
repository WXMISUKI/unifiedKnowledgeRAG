## ADDED Requirements

### Requirement: Provider handoff includes compact Phase 4 caller-consumption smoke evidence

The system SHALL include optional Phase 4 caller-consumption smoke evidence in provider handoff so reviewers can inspect the caller-facing evidence-pack contract coverage without opening the smoke files separately.

#### Scenario: Handoff summarizes caller-consumption smoke

- **WHEN** provider handoff reads the Phase 4 caller-consumption smoke
- **THEN** it summarizes the report status, key checks, and caller allowlist/fail-closed coverage in a compact row

#### Scenario: Missing caller-consumption smoke remains non-blocking

- **WHEN** the optional caller-consumption smoke is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior
