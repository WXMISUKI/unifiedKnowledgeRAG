## ADDED Requirements

### Requirement: Provider handoff can summarize optional BGE-M3 artifact readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional BGE-M3 artifact readiness evidence as read-only deployment context.

#### Scenario: Handoff summarizes artifact readiness

- **WHEN** provider handoff reads the BGE-M3 artifact readiness export
- **THEN** it summarizes report status, decision, checksum coverage, and readiness posture in a compact optional row

#### Scenario: Missing artifact readiness remains non-blocking

- **WHEN** the optional BGE-M3 artifact readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates artifact readiness before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the BGE-M3 artifact readiness export before final handoff bundle generation
