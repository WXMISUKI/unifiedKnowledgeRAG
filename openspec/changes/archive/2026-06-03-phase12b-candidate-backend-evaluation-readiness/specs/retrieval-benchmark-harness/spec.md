## ADDED Requirements

### Requirement: Phase 12b candidate backend evaluation readiness can be exported locally

The system SHALL export a local Phase 12b candidate backend evaluation readiness report that consolidates existing candidate backend evidence into a shared review artifact.

#### Scenario: Evaluation readiness export writes artifacts

- **WHEN** the Phase 12b candidate backend evaluation readiness export runs
- **THEN** the system writes JSON and Markdown evidence files under `docs/operations/candidate-backend-evaluation-readiness/`

#### Scenario: Evaluation readiness summarizes candidate families and open gates

- **WHEN** the export completes
- **THEN** it includes candidate family readouts, shared evidence signals, review-ready families, open gate ids, and reference-only candidates

#### Scenario: Evaluation readiness remains read-only

- **WHEN** the report is exported
- **THEN** runtime defaults, public HTTP APIs, and promotion decisions remain unchanged

### Requirement: Phase 12b candidate backend candidates remain evidence-backed or reference-only

The retrieval benchmark harness SHALL keep candidate backend families as evidence-backed review inputs or reference-only comparisons until a separate promotion change is approved.

#### Scenario: Evidence-backed families remain reversible

- **WHEN** a candidate backend family has enough local evidence for review
- **THEN** the report can mark it `continue_spike` or `eligible_for_promotion_review`
- **AND** the runtime defaults remain unchanged

#### Scenario: Reference-only families do not imply backend integration

- **WHEN** a mature open-source engine is named but no local candidate evidence exists yet
- **THEN** the report records it as `reference_only` and keeps it outside provider backend integration
