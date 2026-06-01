## ADDED Requirements

### Requirement: Provider handoff can summarize optional deployed field validation readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 deployed field validation readiness evidence as read-only review context.

#### Scenario: Handoff summarizes deployed field validation readiness

- **WHEN** provider handoff reads the deployed field validation readiness export
- **THEN** it summarizes report status, decision, and key readiness signals in a compact optional row

#### Scenario: Missing deployed field validation readiness remains non-blocking

- **WHEN** the optional deployed field validation readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates deployed field validation readiness before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates deployed field validation readiness evidence before final handoff bundle generation
