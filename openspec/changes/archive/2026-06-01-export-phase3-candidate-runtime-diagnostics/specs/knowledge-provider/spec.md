## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 3 runtime diagnostics evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 candidate runtime diagnostics evidence as read-only review context.

#### Scenario: Handoff summarizes runtime diagnostics

- **WHEN** provider handoff reads the Phase 3 candidate runtime diagnostics export
- **THEN** it summarizes report status, decision, and prerequisite-check coverage in a compact optional row

#### Scenario: Missing runtime diagnostics remains non-blocking

- **WHEN** the optional Phase 3 candidate runtime diagnostics export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates runtime diagnostics before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Phase 3 candidate runtime diagnostics export before final handoff bundle generation
