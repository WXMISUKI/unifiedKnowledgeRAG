## ADDED Requirements

### Requirement: Provider handoff can summarize optional Qdrant vector-store readiness evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 6 Qdrant vector-store readiness evidence as read-only deployment context.

#### Scenario: Handoff summarizes Qdrant readiness export

- **WHEN** provider handoff reads the Qdrant vector-store readiness export
- **THEN** it summarizes report status, decision, and key readiness signals in a compact optional row

#### Scenario: Missing Qdrant readiness export remains non-blocking

- **WHEN** the optional Qdrant vector-store readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates Qdrant readiness before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Qdrant vector-store readiness export before final handoff bundle generation
