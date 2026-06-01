## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 3 aggregation/relation negative-control smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 aggregation/relation negative-control smoke evidence as read-only review context.

#### Scenario: Handoff summarizes negative-control smoke

- **WHEN** provider handoff reads the Phase 3 aggregation/relation negative-control smoke export
- **THEN** it summarizes report status, decision, positive control, negative control, and relation-aware grading alignment in a compact optional row

#### Scenario: Missing negative-control smoke remains non-blocking

- **WHEN** the optional aggregation/relation negative-control smoke export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates negative-control smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Phase 3 aggregation/relation negative-control smoke export before final handoff bundle generation
