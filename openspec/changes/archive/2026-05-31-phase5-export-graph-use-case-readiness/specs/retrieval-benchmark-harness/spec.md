## ADDED Requirements

### Requirement: Phase 5 graph use-case readiness can be exported

The system SHALL export a local Phase 5 graph use-case readiness report that summarizes the graph use-case contract, provider preflight graph boundary evidence, and the next evidence needed for GraphRAG boundary review.

#### Scenario: Readiness report is exported

- **WHEN** the Phase 5 graph readiness export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/graph-use-case-readiness/`

#### Scenario: Readiness report summarizes current evidence

- **WHEN** the export completes
- **THEN** the report summarizes the graph use-case contract, graph schema discovery, and the planned graph query boundary

#### Scenario: Readiness export remains read-only

- **WHEN** the readiness report is exported
- **THEN** runtime retrieval defaults, caller ownership, and provider HTTP contracts remain unchanged
