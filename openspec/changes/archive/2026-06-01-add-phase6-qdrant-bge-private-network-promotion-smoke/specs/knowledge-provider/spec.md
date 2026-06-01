## ADDED Requirements

### Requirement: Provider handoff can summarize optional private-network promotion smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 private-network promotion smoke evidence as read-only review context.

#### Scenario: Handoff summarizes private-network smoke

- **WHEN** provider handoff reads private-network promotion smoke evidence
- **THEN** it summarizes smoke status and check coverage in a compact optional row

#### Scenario: Missing private-network smoke remains non-blocking

- **WHEN** the optional private-network promotion smoke artifact is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates private-network smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates private-network promotion smoke evidence before final handoff bundle generation
