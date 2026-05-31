## ADDED Requirements

### Requirement: Phase 3 retrieval promotion readiness can be exported

The system SHALL export a local Phase 3 retrieval promotion readiness report that summarizes current promotion gates, open gaps, and the next evidence needed for review.

#### Scenario: Readiness report is exported

- **WHEN** the Phase 3 readiness export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/retrieval-promotion-readiness/`

#### Scenario: Readiness report summarizes current gates

- **WHEN** the export completes
- **THEN** the report summarizes Qdrant, BGE-M3, hybrid retrieval, hybrid gating, multi-chunk aggregation, relation-aware grading, and deployed smoke

#### Scenario: Readiness export remains read-only

- **WHEN** the readiness report is exported
- **THEN** runtime retrieval defaults, provider HTTP contracts, and promotion gates remain unchanged
