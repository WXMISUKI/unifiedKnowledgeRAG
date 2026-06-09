## ADDED Requirements

### Requirement: Provider expansion pauses after onboarding and evidence closure until a new trigger appears
The project SHALL treat the current provider state as paused for further feature expansion after onboarding, evidence, and catalog closure unless a stronger follow-up trigger appears.

#### Scenario: Closed provider baseline defaults to no new provider slice
- **WHEN** the current provider baseline includes passing onboarding validation examples, onboarding discovery, pack discovery, and existing failed-question evidence
- **THEN** the default next action is to pause provider-side expansion
- **AND** future provider changes require an explicit trigger condition

#### Scenario: Lack of trigger blocks speculative strategy work
- **WHEN** no new real caller feedback, repeated failure class, or provider-owned gap is available
- **THEN** the roadmap does not open query rewrite, rerank, hybrid retrieval, GraphRAG, or further provider-side feature work by default

### Requirement: Only explicit trigger classes can reopen provider-side feature work
The project SHALL require future provider-side feature changes to declare an explicit trigger class before expansion resumes.

#### Scenario: Real caller feedback can reopen provider work
- **WHEN** a real caller trial exposes a concrete provider-owned gap
- **THEN** a future change can use `real_caller_feedback_trigger` or `provider_owned_gap_trigger`
- **AND** the change describes why the issue belongs to this provider rather than the caller or control plane

#### Scenario: Repeated cross-source failure class can reopen hardening work
- **WHEN** failed-question evidence shows a repeated and accepted failure class across more than one source
- **THEN** a future change can use `repeated_cross_source_failure_class_trigger`
- **AND** the change remains narrowly scoped to that failure class

#### Scenario: Runtime-strategy evaluation requires stronger evidence
- **WHEN** a future change proposes query rewrite, rerank, hybrid retrieval, GraphRAG, or another advanced retrieval strategy
- **THEN** it uses `runtime_strategy_evaluation_trigger`
- **AND** it references repeated real failure evidence rather than popularity or curiosity alone

### Requirement: Caller and control-plane concerns do not reopen provider work by default
The project SHALL keep caller-side orchestration and control-plane responsibilities outside this provider when evaluating new work triggers.

#### Scenario: Caller-owned concerns do not qualify as provider trigger
- **WHEN** a new issue concerns final answer policy, source-to-agent binding policy, permissions, approvals, audit governance, or caller orchestration
- **THEN** it does not qualify as a provider-side expansion trigger by default
- **AND** the roadmap keeps that work outside this repository
