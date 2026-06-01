## ADDED Requirements

### Requirement: Phase 8 live URL smoke consistency check remains evidence-only

The project SHALL treat Phase 8 live URL smoke consistency check as local evidence-drift detection without changing runtime defaults.

#### Scenario: Smoke compares readiness and handoff summary

- **WHEN** the Phase 8 smoke report is generated
- **THEN** it compares readiness status and key summary fields against the handoff bundle row

#### Scenario: Mismatch is visible but not runtime promotion

- **WHEN** any readiness-vs-handoff field is inconsistent
- **THEN** the smoke is blocked and does not imply runtime default promotion changes
