## ADDED Requirements

### Requirement: Post-closure caller trial feedback runbook is the default execution entrypoint
The project SHALL provide a post-closure caller trial feedback runbook so teams can execute the real caller-trial workflow in order instead of reopening provider-side feature work by default.

#### Scenario: Runbook sequences the post-closure path
- **WHEN** the provider baseline is closed and the caller trial outcome input contract already exists
- **THEN** the project provides a runbook that sequences Phase 15 dispatch review, Phase 16 access review, caller-side trial execution, caller-side outcome export, and Phase 25 provider feedback consumption

#### Scenario: Runbook does not reopen provider features by itself
- **WHEN** teams use the runbook after provider closure
- **THEN** the default action remains real caller trial execution and feedback capture
- **AND** the roadmap does not reopen query rewrite, rerank, hybrid retrieval, GraphRAG, or other provider-side feature work by default
