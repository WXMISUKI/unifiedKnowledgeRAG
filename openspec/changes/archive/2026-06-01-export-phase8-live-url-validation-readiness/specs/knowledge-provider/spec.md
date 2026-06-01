## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 8 live URL validation readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 8 live URL validation readiness evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 8 readiness

- **WHEN** provider handoff reads the Phase 8 readiness export
- **THEN** it summarizes live validation state, decision, deployed smoke posture, live URL presence, and open-gate count

#### Scenario: Missing Phase 8 readiness remains non-blocking

- **WHEN** optional Phase 8 readiness evidence is missing
- **THEN** handoff marks it reviewable and preserves required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 8 readiness before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 8 readiness before final provider handoff bundle generation
