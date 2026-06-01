## ADDED Requirements

### Requirement: Phase 3 candidate latency/resource diagnostics can be exported locally

The system SHALL export a local Phase 3 candidate latency/resource diagnostics report that combines benchmark latency profile evidence with resource/deployment posture evidence.

#### Scenario: Latency/resource diagnostics are exported

- **WHEN** the Phase 3 latency/resource diagnostics export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/`

#### Scenario: Latency/resource diagnostics summarize current evidence

- **WHEN** the export completes
- **THEN** the report summarizes benchmark latency statistics, deployment readiness posture, runtime diagnostics posture, and the current resource snapshot

#### Scenario: Latency/resource diagnostics remain read-only

- **WHEN** the latency/resource diagnostics report is exported
- **THEN** runtime defaults, public HTTP APIs, and promotion decisions remain unchanged
