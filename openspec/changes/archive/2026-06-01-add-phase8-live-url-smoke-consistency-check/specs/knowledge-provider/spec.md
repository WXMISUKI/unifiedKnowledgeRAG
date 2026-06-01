## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 8 live URL smoke consistency evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 8 live URL smoke consistency evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 8 smoke

- **WHEN** provider handoff reads the Phase 8 smoke export
- **THEN** it summarizes smoke status, decision, check pass/fail counts, and readiness/bundle alignment context

#### Scenario: Missing Phase 8 smoke remains non-blocking

- **WHEN** optional Phase 8 smoke evidence is missing
- **THEN** handoff marks it reviewable and preserves required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 8 smoke before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 8 smoke after Phase 8 readiness and before final provider handoff bundle generation
