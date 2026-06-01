## ADDED Requirements

### Requirement: Provider handoff can summarize optional Qdrant backup/restore smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 Qdrant backup/restore smoke evidence as read-only operations context.

#### Scenario: Handoff summarizes backup/restore smoke

- **WHEN** provider handoff reads the Qdrant backup/restore smoke export
- **THEN** it summarizes smoke status and check coverage in a compact optional row

#### Scenario: Missing backup/restore smoke remains non-blocking

- **WHEN** the optional Qdrant backup/restore smoke export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates backup/restore smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Qdrant backup/restore smoke export before final handoff bundle generation
