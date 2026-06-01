## ADDED Requirements

### Requirement: Phase 3 hybrid cross-case FP/FN smoke can be exported locally

The system SHALL export a local Phase 3 hybrid cross-case FP/FN smoke report that validates cross-case risk-signal visibility from existing benchmark and FP/FN evidence.

#### Scenario: Cross-case smoke export writes artifacts

- **WHEN** the Phase 3 hybrid cross-case FP/FN smoke export runs
- **THEN** it writes JSON and Markdown evidence files under `docs/smoke/hybrid-cross-case-fp-fn/`

#### Scenario: Cross-case smoke validates risk-signal alignment

- **WHEN** the smoke runs
- **THEN** it validates baseline risk-case coverage, false-positive trap alignment, and key positive-control case outcomes

#### Scenario: Cross-case smoke remains read-only

- **WHEN** cross-case smoke is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and promotion decisions remain unchanged
