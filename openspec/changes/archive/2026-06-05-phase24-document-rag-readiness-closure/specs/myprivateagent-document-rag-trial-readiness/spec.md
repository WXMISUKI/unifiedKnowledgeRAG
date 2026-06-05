## ADDED Requirements

### Requirement: Provider publishes document RAG trial readiness closure
The system SHALL publish a read-only Phase 24 closure report that summarizes whether the configured provider evidence is ready for a MyPrivateAgent document RAG repo-side trial.

#### Scenario: Primitive access evidence is ready
- **WHEN** the provider contract smoke and Phase 10/11 primitive access smokes are present and ready
- **THEN** the Phase 24 closure report has `status=ready`, `decision=go`, and recommends beginning the MyPrivateAgent repo-side document RAG trial

#### Scenario: Primitive access evidence is blocked
- **WHEN** any required primitive access signal is missing or blocked
- **THEN** the Phase 24 closure report has `status=blocked`, `decision=blocked`, and identifies the blocked signal ids

#### Scenario: Review-only context remains visible
- **WHEN** optional readiness, handoff, or access-loop evidence is present with `review` status
- **THEN** the Phase 24 closure report lists those signals as review context without blocking the primitive trial gate

### Requirement: Trial readiness closure remains provider-side and read-only
The Phase 24 closure report SHALL preserve provider/caller ownership boundaries and SHALL NOT mutate runtime behavior.

#### Scenario: Closure report is exported
- **WHEN** the Phase 24 export command runs
- **THEN** it writes machine-readable JSON and Markdown evidence files without starting a server, changing retrieval defaults, executing source binding, rebuilding indexes, downloading models, or executing GraphRAG

#### Scenario: Caller ownership remains explicit
- **WHEN** a caller reads the Phase 24 closure report
- **THEN** the report states that MyPrivateAgent owns repo-side trial execution, source-to-agent binding, audit policy, and final answer behavior
