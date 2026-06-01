## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 2 unsupported-format negative-control smoke

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 2 unsupported-format negative-control smoke evidence as read-only review context.

#### Scenario: Handoff summarizes Phase 2 unsupported-format smoke

- **WHEN** provider handoff reads the Phase 2 unsupported-format negative-control smoke export
- **THEN** it summarizes smoke status, decision, check pass/fail counts, and unsupported/non-markdown counters in an optional row

#### Scenario: Missing Phase 2 unsupported-format smoke remains non-blocking

- **WHEN** the optional Phase 2 unsupported-format negative-control smoke export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates Phase 2 unsupported-format smoke before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 2 unsupported-format negative-control smoke after Phase 2 source-format demand readiness and before final handoff bundle generation
