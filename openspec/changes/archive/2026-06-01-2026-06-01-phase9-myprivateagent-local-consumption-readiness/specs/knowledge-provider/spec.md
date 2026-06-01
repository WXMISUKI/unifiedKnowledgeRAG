## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 9 MyPrivateAgent local-consumption evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 9 MyPrivateAgent local-consumption readiness and smoke evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 9 readiness and smoke

- **WHEN** provider handoff reads Phase 9 local-consumption readiness and smoke exports
- **THEN** it summarizes local-consumption state, decision, control-plane hint alignment, and open-gate context

#### Scenario: Missing Phase 9 evidence remains non-blocking

- **WHEN** optional Phase 9 local-consumption readiness/smoke evidence is missing
- **THEN** handoff marks it reviewable and preserves required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 9 evidence before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 9 local-consumption readiness and smoke before final provider handoff bundle generation
