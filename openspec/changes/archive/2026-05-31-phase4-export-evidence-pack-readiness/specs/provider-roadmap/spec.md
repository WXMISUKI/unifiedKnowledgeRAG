## MODIFIED Requirements

### Requirement: Evidence packaging changes advance Phase 4 without changing provider scope

The project SHALL treat retrieval evidence packs, citation policy metadata, insufficient-evidence diagnostics, caller consumption contracts, and readiness exports as Phase 4 roadmap work when they help callers answer safely without moving final answer policy into the provider.

#### Scenario: Evidence packaging is phase-aligned

- **WHEN** an OpenSpec change adds evidence pack metadata, a caller consumption contract, or a readiness export for RAG retrieve or answer envelopes
- **THEN** the change identifies Phase 4 as the roadmap phase it advances

#### Scenario: Evidence packaging does not imply answer policy ownership

- **WHEN** the provider exposes evidence status, allowed citations, caller consumption rules, or readiness summaries
- **THEN** the roadmap boundary still states that the caller owns final user-facing answer style, refusal policy, and workflow decisions
