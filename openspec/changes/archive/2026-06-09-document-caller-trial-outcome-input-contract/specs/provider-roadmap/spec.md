## ADDED Requirements

### Requirement: Real caller feedback input contract is stabilized before reopening provider work
The project SHALL define a minimal caller-side live trial outcome input contract before treating future provider follow-up as a stable trigger-driven workflow.

#### Scenario: Caller feedback contract is phase-aligned
- **WHEN** the provider already has dispatch, access-loop, and feedback-closure artifacts
- **THEN** the next practical slice may define the minimal caller trial outcome input contract
- **AND** it is treated as feedback-closure infrastructure rather than new provider feature expansion

#### Scenario: Caller feedback contract does not reopen provider strategy work
- **WHEN** the project documents caller trial outcome input expectations
- **THEN** it does not by itself reopen query rewrite, rerank, hybrid retrieval, GraphRAG, or other provider-side strategy work

### Requirement: Caller feedback contract preserves provider/caller ownership boundaries
The project SHALL keep the caller trial outcome input contract lightweight and boundary-safe.

#### Scenario: Input contract preserves caller ownership
- **WHEN** the contract defines fields such as caller status, provider retrieve facts, and evidence-pack summary
- **THEN** MyPrivateAgent or another caller still owns trial execution, final answer policy, source binding policy, and audit behavior

#### Scenario: Input contract preserves provider ownership
- **WHEN** the provider consumes the caller trial outcome file
- **THEN** it only classifies provider follow-up posture
- **AND** it does not execute the caller, create bindings, or mutate runtime defaults
