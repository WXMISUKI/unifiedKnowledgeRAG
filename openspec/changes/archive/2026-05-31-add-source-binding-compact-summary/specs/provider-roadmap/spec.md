## ADDED Requirements

### Requirement: Source binding compact summaries stay lightweight

The project SHALL treat source binding aggregate counts as lightweight Phase 2 and Phase 6 evidence when they summarize existing source readiness rows without changing binding policy or executing provider capabilities.

#### Scenario: Source binding compact summary is phase-aligned

- **WHEN** an OpenSpec change adds compact counts to source binding evidence
- **THEN** the roadmap records it as source readiness and handoff evidence rather than source-to-agent binding execution

#### Scenario: Source binding compact summary preserves provider boundary

- **WHEN** source binding compact counts are generated
- **THEN** binding policy, approvals, audit, registration, final answer workflow, ingestion execution, retrieval execution, and GraphRAG execution remain outside this provider
