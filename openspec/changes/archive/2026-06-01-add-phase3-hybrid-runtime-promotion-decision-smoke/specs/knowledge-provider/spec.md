## ADDED Requirements

### Requirement: Provider handoff can summarize optional hybrid runtime promotion decision smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 hybrid runtime promotion decision smoke evidence as read-only review context.

#### Scenario: Handoff summarizes hybrid decision smoke

- **WHEN** provider handoff reads hybrid runtime promotion decision smoke evidence
- **THEN** it summarizes smoke status and check coverage in a compact optional row

#### Scenario: Missing hybrid decision smoke remains non-blocking

- **WHEN** the optional hybrid runtime promotion decision smoke artifact is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates hybrid decision smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates hybrid runtime promotion decision smoke evidence before final handoff bundle generation
