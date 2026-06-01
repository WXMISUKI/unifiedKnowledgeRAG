## ADDED Requirements

### Requirement: Provider handoff can summarize optional private-network promotion readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 Qdrant+BGE-M3 private-network promotion readiness evidence as read-only review context.

#### Scenario: Handoff summarizes private-network readiness

- **WHEN** provider handoff reads the private-network promotion readiness export
- **THEN** it summarizes report status, decision, and key open-gate counts in a compact optional row

#### Scenario: Missing private-network readiness remains non-blocking

- **WHEN** the optional private-network promotion readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates private-network readiness before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the private-network promotion readiness export before final handoff bundle generation
