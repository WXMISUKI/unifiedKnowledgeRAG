## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 2 source-format demand readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 2 source-format demand readiness evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 2 readiness

- **WHEN** provider handoff reads the Phase 2 source-format demand readiness export
- **THEN** it summarizes report status, decision, demand signal, and open-gate count in a compact optional row

#### Scenario: Missing Phase 2 readiness remains non-blocking

- **WHEN** the optional Phase 2 source-format demand readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 2 readiness before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Phase 2 source-format demand readiness export after source binding summary and before final handoff bundle generation
