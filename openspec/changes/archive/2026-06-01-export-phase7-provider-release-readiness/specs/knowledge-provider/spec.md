## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 7 release-readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 7 provider release-readiness evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 7 release-readiness

- **WHEN** provider handoff reads the Phase 7 release-readiness export
- **THEN** it summarizes release state, decision, local-handoff readiness, runtime-promotion readiness, and open-gate count

#### Scenario: Missing Phase 7 release-readiness remains non-blocking

- **WHEN** optional Phase 7 release-readiness evidence is missing
- **THEN** handoff marks it reviewable and preserves required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 7 release-readiness before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 7 release-readiness before final provider handoff bundle generation
