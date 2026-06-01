## ADDED Requirements

### Requirement: Provider handoff can summarize optional hybrid runtime promotion decision readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 hybrid runtime promotion decision readiness evidence as read-only review context.

#### Scenario: Handoff summarizes hybrid decision readiness

- **WHEN** provider handoff reads hybrid runtime promotion decision readiness evidence
- **THEN** it summarizes report status, decision, and open-gate counts in a compact optional row

#### Scenario: Missing hybrid decision readiness remains non-blocking

- **WHEN** the optional hybrid runtime promotion decision readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates hybrid decision readiness before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates hybrid runtime promotion decision readiness evidence before Phase 4 and final handoff bundle steps
