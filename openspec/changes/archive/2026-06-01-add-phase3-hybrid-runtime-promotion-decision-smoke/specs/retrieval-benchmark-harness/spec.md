## ADDED Requirements

### Requirement: Phase 3 hybrid runtime promotion decision smoke can be exported locally

The system SHALL export a local Phase 3 hybrid runtime promotion decision smoke report that validates final decision evidence-chain completeness.

#### Scenario: Hybrid decision smoke export writes artifacts

- **WHEN** the Phase 3 hybrid runtime promotion decision smoke export runs
- **THEN** it writes JSON and Markdown evidence files under `docs/smoke/hybrid-runtime-promotion/`

#### Scenario: Hybrid decision smoke validates readiness linkage

- **WHEN** the smoke runs
- **THEN** it validates contract/readiness artifacts plus required Phase 3 and Phase 6 bridge evidence presence and parseability

#### Scenario: Hybrid decision smoke remains read-only

- **WHEN** smoke artifacts are exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and promotion decisions remain unchanged
