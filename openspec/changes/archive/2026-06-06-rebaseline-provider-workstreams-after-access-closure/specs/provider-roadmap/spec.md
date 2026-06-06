# provider-roadmap Specification

## MODIFIED Requirements

### Requirement: Provider roadmap defines phase gates
The project SHALL define phase gates with concrete outcomes and evidence so future OpenSpec changes can be selected by project value rather than local optimization alone.

#### Scenario: Future changes identify a phase
- **WHEN** a future OpenSpec change is proposed
- **THEN** it identifies the roadmap phase it advances or explains why it is outside the staged roadmap

#### Scenario: Runtime promotion requires evidence
- **WHEN** a future change promotes a candidate retrieval mode, embedding model, vector-store behavior, reranker, answer composer, or GraphRAG behavior into a runtime default
- **THEN** it references machine-readable evidence or explicitly records the missing evidence as an open gate

#### Scenario: Candidate work stays reversible
- **WHEN** a future change adds evaluation-only or candidate-only behavior
- **THEN** it avoids changing default runtime behavior unless the relevant phase gate says promotion criteria are met

#### Scenario: Phase 25 closes caller trial feedback without expanding readiness
- **WHEN** MyPrivateAgent provides a live trial outcome after Phase 24 readiness returned `go`
- **THEN** the roadmap treats Phase 25 as a feedback-closure slice that records provider follow-up posture
- **AND** it does not create another readiness gate, execute the caller trial, promote runtime defaults, or move caller control-plane responsibilities into the provider

#### Scenario: Post-access changes declare a trigger condition
- **WHEN** a future OpenSpec change is proposed after the provider workstream rebaseline
- **THEN** it declares a trigger condition such as real trial bug, corpus/parser demand, backend promotion evidence, deployment-owner request, graph-heavy use case, or explicit maintenance rationale
- **AND** it does not continue the access-readiness phase chain unless the trigger is a real caller trial issue
