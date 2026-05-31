## ADDED Requirements

### Requirement: Source binding coverage advances lightweight evidence review

The project SHALL treat source binding coverage summaries as Phase 2 and Phase 6 bridge work when they expose existing citation, chunk, and parser readiness evidence without adding parser, indexing, retrieval, answer composition, or GraphRAG responsibilities.

#### Scenario: Coverage summary is phase-aligned

- **WHEN** an OpenSpec change adds citation, chunk, or parser coverage counts to source binding review
- **THEN** the roadmap records it as lightweight evidence review that supports enterprise ingestion and external binding readiness

#### Scenario: Coverage summary preserves provider boundary

- **WHEN** source binding coverage is exposed through API or handoff evidence
- **THEN** source-to-agent binding policy, approvals, audit, parser expansion, ingestion execution, and final answer workflow remain owned outside this provider
