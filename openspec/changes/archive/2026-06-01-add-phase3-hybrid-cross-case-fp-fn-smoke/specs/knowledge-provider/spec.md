## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 3 cross-case FP/FN smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 hybrid cross-case FP/FN smoke evidence as read-only review context.

#### Scenario: Handoff summarizes cross-case smoke

- **WHEN** provider handoff reads the Phase 3 hybrid cross-case FP/FN smoke export
- **THEN** it summarizes smoke status and cross-case check coverage in a compact optional row

#### Scenario: Missing cross-case smoke remains non-blocking

- **WHEN** the optional cross-case smoke export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates cross-case smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 3 hybrid cross-case FP/FN smoke evidence before final handoff bundle generation
