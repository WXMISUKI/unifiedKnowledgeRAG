## ADDED Requirements

### Requirement: Provider handoff can summarize optional BGE-M3 comparison smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 BGE-M3 comparison smoke evidence as read-only review context.

#### Scenario: Handoff summarizes comparison smoke

- **WHEN** provider handoff reads the BGE-M3 comparison smoke export
- **THEN** it summarizes smoke status and check coverage in a compact optional row

#### Scenario: Missing comparison smoke remains non-blocking

- **WHEN** the optional BGE-M3 comparison smoke export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates comparison smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the BGE-M3 comparison smoke export before final handoff bundle generation
