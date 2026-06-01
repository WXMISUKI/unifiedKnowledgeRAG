## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 3 candidate latency/resource diagnostics evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 candidate latency/resource diagnostics evidence as read-only review context.

#### Scenario: Handoff summarizes latency/resource diagnostics

- **WHEN** provider handoff reads the Phase 3 candidate latency/resource diagnostics export
- **THEN** it summarizes report status, decision, latency profile, and resource posture in a compact optional row

#### Scenario: Missing latency/resource diagnostics remains non-blocking

- **WHEN** the optional latency/resource diagnostics export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates latency/resource diagnostics before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Phase 3 candidate latency/resource diagnostics export before final handoff bundle generation
