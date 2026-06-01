## ADDED Requirements

### Requirement: Phase 3 hybrid runtime promotion decision readiness can be exported locally

The system SHALL export a local Phase 3 hybrid runtime promotion decision readiness report that consolidates final promotion-review prerequisites.

#### Scenario: Hybrid decision readiness export writes artifacts

- **WHEN** the Phase 3 hybrid runtime promotion decision readiness export runs
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/hybrid-runtime-promotion/`

#### Scenario: Hybrid decision readiness summarizes required signals

- **WHEN** the export completes
- **THEN** it summarizes contract presence, Phase 3 evidence status, Phase 6 bridge evidence status, and open gates with recommended actions

#### Scenario: Hybrid decision readiness remains read-only

- **WHEN** the report is exported
- **THEN** runtime defaults, public HTTP APIs, and promotion decisions remain unchanged
