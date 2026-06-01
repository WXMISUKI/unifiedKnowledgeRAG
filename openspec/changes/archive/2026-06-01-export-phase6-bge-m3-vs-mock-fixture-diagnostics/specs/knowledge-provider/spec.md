## ADDED Requirements

### Requirement: Provider handoff can summarize optional BGE-M3 comparison diagnostics evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 BGE-M3 comparison diagnostics evidence as read-only review context.

#### Scenario: Handoff summarizes comparison diagnostics

- **WHEN** provider handoff reads the BGE-M3 comparison diagnostics export
- **THEN** it summarizes report status, decision, and key comparison signal counts in a compact optional row

#### Scenario: Missing comparison diagnostics remains non-blocking

- **WHEN** the optional BGE-M3 comparison diagnostics export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates comparison diagnostics before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the BGE-M3 comparison diagnostics export before final handoff bundle generation
