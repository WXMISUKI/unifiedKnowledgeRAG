## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 7 cross-phase consistency smoke

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 7 cross-phase consistency smoke evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 7 cross-phase consistency smoke

- **WHEN** provider handoff reads the Phase 7 cross-phase consistency smoke export
- **THEN** it summarizes smoke status, decision, and check pass/fail counts in an optional row

#### Scenario: Missing Phase 7 cross-phase consistency smoke remains non-blocking

- **WHEN** optional Phase 7 cross-phase consistency smoke evidence is missing
- **THEN** handoff marks it reviewable and preserves required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 7 cross-phase consistency smoke before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 7 cross-phase consistency smoke after Phase 7 release-readiness and before final handoff bundle generation
