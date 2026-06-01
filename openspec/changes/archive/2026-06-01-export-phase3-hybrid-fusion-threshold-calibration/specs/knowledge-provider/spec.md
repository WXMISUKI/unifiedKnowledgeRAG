## ADDED Requirements

### Requirement: Provider handoff can summarize optional Phase 3 hybrid fusion calibration evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 hybrid fusion/threshold calibration evidence as read-only review context.

#### Scenario: Handoff summarizes calibration evidence

- **WHEN** provider handoff reads the Phase 3 hybrid fusion/threshold calibration export
- **THEN** it summarizes report status, decision, and calibration signal counts in a compact optional row

#### Scenario: Missing calibration evidence remains non-blocking

- **WHEN** the optional Phase 3 hybrid fusion/threshold calibration export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates calibration evidence before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Phase 3 hybrid fusion/threshold calibration export before final handoff bundle generation
