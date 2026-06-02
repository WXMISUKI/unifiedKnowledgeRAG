## ADDED Requirements

### Requirement: Handoff evidence can summarize optional Phase 11 local integration dry-run artifacts

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 11 local integration profile/discovery/retrieve/source-binding preview artifacts as read-only review context.

#### Scenario: Handoff summarizes Phase 11 dry-run artifact states

- **WHEN** provider handoff reads Phase 11 artifacts
- **THEN** it summarizes local integration profile state, discovery smoke state, retrieval-consumption smoke state, and source-binding preview smoke state

#### Scenario: Missing Phase 11 artifacts are reviewable

- **WHEN** optional Phase 11 artifacts are missing
- **THEN** handoff marks them as reviewable optional evidence and keeps required-artifact behavior unchanged

#### Scenario: Refresh regenerates Phase 11 artifacts before final handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 11 local integration artifacts before final provider handoff bundle generation
