## ADDED Requirements

### Requirement: Phase 3 hybrid fusion/threshold calibration can be exported locally

The system SHALL export a local Phase 3 hybrid fusion/threshold calibration report that summarizes candidate calibration evidence without changing runtime behavior.

#### Scenario: Calibration export writes artifacts

- **WHEN** the Phase 3 hybrid fusion/threshold calibration export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/`

#### Scenario: Calibration export summarizes hybrid and threshold context

- **WHEN** the export completes
- **THEN** the report includes hybrid exact-term evidence, hybrid empty-stress evidence, hybrid gate evidence, threshold recommendation/sweep context, FP/FN review context, and deployment runtime threshold context

#### Scenario: Calibration export remains read-only

- **WHEN** the calibration report is exported
- **THEN** runtime defaults, public HTTP APIs, and promotion decisions remain unchanged
