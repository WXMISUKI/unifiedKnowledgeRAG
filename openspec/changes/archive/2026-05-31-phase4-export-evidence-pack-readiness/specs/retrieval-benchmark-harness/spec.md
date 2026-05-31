## ADDED Requirements

### Requirement: Phase 4 evidence pack readiness can be exported

The system SHALL export a local Phase 4 evidence pack readiness report that summarizes the stable `evidence_pack-v1` contract coverage, provider contract smoke coverage, and the next evidence needed for caller-consumption review.

#### Scenario: Readiness report is exported

- **WHEN** the Phase 4 readiness export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/evidence-pack-readiness/`

#### Scenario: Readiness report summarizes current evidence

- **WHEN** the export completes
- **THEN** the report summarizes the contract document, provider contract smoke status, and the existing fail-closed evidence-pack semantics

#### Scenario: Readiness export remains read-only

- **WHEN** the readiness report is exported
- **THEN** runtime retrieval defaults, caller ownership, and provider HTTP contracts remain unchanged
