## ADDED Requirements

### Requirement: Source binding summary exposes compact aggregate counts

The system SHALL include compact aggregate counts in the source binding summary response so external control planes can quickly review binding readiness without recomputing common totals from source rows.

#### Scenario: Source binding response includes aggregate counts

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the response includes `total_source_count`, `bindable_source_count`, `status_counts`, and `recommended_action_counts` derived from the returned source rows

#### Scenario: Source binding aggregate counts remain evidence-only

- **WHEN** the provider builds source binding aggregate counts
- **THEN** it does not create source-to-agent bindings, run approvals, write audit records, create ingestion jobs, rebuild indexes, execute retrieval, compose answers, or execute GraphRAG

#### Scenario: Source binding export includes aggregate counts

- **WHEN** a caller exports source binding evidence
- **THEN** the JSON and Markdown outputs include the compact aggregate counts alongside the detailed source rows
