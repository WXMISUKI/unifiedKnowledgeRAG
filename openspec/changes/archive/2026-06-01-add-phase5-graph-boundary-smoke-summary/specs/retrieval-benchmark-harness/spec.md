## ADDED Requirements

### Requirement: Phase 5 graph boundary smoke summaries can be exported

The system SHALL export a local Phase 5 graph boundary smoke summary that consolidates graph schema discovery and the planned graph query boundary into a compact read-only report.

#### Scenario: Smoke summary is exported

- **WHEN** the Phase 5 graph boundary smoke export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/smoke/graph-boundary-summary/`

#### Scenario: Smoke summary summarizes current evidence

- **WHEN** the export completes
- **THEN** the summary captures graph schema discovery, graph store labels, and the planned graph query boundary

#### Scenario: Smoke summary remains read-only

- **WHEN** the summary is exported
- **THEN** runtime retrieval defaults, caller ownership, and provider HTTP contracts remain unchanged
