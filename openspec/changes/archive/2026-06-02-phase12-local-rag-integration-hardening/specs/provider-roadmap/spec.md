## ADDED Requirements

### Requirement: Local RAG integration hardening precedes backend migration

The project SHALL complete a local MyPrivateAgent RAG integration hardening slice before considering any retrieval backend migration.

#### Scenario: Local integration hardening is the short-term acceptance gate

- **WHEN** short-term roadmap execution is planned
- **THEN** it must execute the local MyPrivateAgent RAG integration hardening slice
- **AND** it keeps endpoint contracts, evidence-pack semantics, and local API assumptions explicit and stable

#### Scenario: Local hardening remains read-only

- **WHEN** hardening artifacts are executed locally
- **THEN** they remain read-only exports or smoke checks
- **AND** runtime retrieval defaults, GraphRAG execution, and parser defaults remain unchanged

### Requirement: Local RAG integration hardening surfaces explicit assumptions

The project SHALL expose short-term local integration assumptions as explicit evidence inputs and not implicit environment behavior.

#### Scenario: Local integration assumptions are explicit

- **WHEN** the hardening profile is exported
- **THEN** it records local base URL, API-key mode (`not_configured_local_dev` or `provider_key_protected_api`), and required smoke dependencies

#### Scenario: Source and policy boundaries remain explicit

- **WHEN** integration hardening is reviewed
- **THEN** it states that source-to-agent binding, final answer policy, and caller orchestration remain external caller responsibilities

### Requirement: Local retrieve consumption remains fail-closed

The project SHALL keep local retrieval consumption checks constrained to fail-closed evidence behavior.

#### Scenario: Fail-closed local retrieval behavior is preserved

- **WHEN** retrieval return is empty or insufficient
- **THEN** `insufficient_evidence` + reason and `use_only_returned_citations` behavior is preserved and exported for local integration review

#### Scenario: Hardening smoke validates consumption contracts

- **WHEN** hardening smoke runs
- **THEN** it checks phase4 caller-consumption readiness and provider contract smoke alignment
- **AND** it records a local integration verdict without mutating runtime behavior
