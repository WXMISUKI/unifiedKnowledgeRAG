## ADDED Requirements

### Requirement: Source binding aggregate reuse stays lightweight

The project SHALL treat reuse of source binding aggregate counts in handoff and deployed-smoke evidence as lightweight Phase 2 and Phase 6 consistency work when it avoids duplicated aggregation without changing provider scope.

#### Scenario: Aggregate reuse is phase-aligned

- **WHEN** an OpenSpec change makes evidence summaries prefer source binding aggregate counts
- **THEN** the roadmap records it as source readiness and handoff consistency evidence rather than source-to-agent binding execution

#### Scenario: Aggregate reuse preserves provider boundary

- **WHEN** handoff or deployed-smoke evidence reuses source binding aggregate counts
- **THEN** binding policy, approvals, audit, registration, final answer workflow, ingestion execution, retrieval execution, and GraphRAG execution remain outside this provider
