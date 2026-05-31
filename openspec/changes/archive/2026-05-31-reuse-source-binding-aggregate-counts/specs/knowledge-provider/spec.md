## ADDED Requirements

### Requirement: Source binding aggregate counts are reused by evidence summaries

The system SHALL prefer provider-owned source binding aggregate counts when handoff and deployed-smoke evidence summarize source binding readiness.

#### Scenario: Handoff summary reuses source binding aggregate counts

- **WHEN** the provider handoff bundle reads source binding evidence that includes `total_source_count`, `bindable_source_count`, `status_counts`, and `recommended_action_counts`
- **THEN** the `source_binding_summary` artifact summary uses those aggregate values instead of recomputing them from source rows

#### Scenario: Deployed smoke reuses source binding aggregate counts

- **WHEN** the deployed provider smoke probe reads a source binding response that includes aggregate count fields
- **THEN** the `provider_source_bindings` check details use those aggregate values

#### Scenario: Older source binding evidence remains compatible

- **WHEN** handoff or deployed-smoke source binding evidence does not include aggregate count fields
- **THEN** the system falls back to deriving counts from returned source rows

#### Scenario: Aggregate count reuse remains read-only

- **WHEN** source binding aggregate counts are reused by evidence summaries
- **THEN** the system does not create source-to-agent bindings, run approvals, write audit records, create ingestion jobs, rebuild indexes, execute retrieval, compose answers, or execute GraphRAG
