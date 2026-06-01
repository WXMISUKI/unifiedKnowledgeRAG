## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 10 MyPrivateAgent local consumer verification evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 10 MyPrivateAgent local consumer readiness and probe evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 10 readiness and probe evidence

- **WHEN** provider handoff reads Phase 10 local consumer readiness and probe exports
- **THEN** it summarizes local consumer verification state, recommended base URL, access-key posture, graph boundary alignment, evidence-pack readiness, and runtime-promotion boundary status

#### Scenario: Missing Phase 10 evidence remains non-blocking

- **WHEN** optional Phase 10 local consumer readiness/probe evidence is missing
- **THEN** handoff marks it reviewable and preserves required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 10 evidence before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 10 local consumer readiness and probe evidence before final provider handoff bundle generation
