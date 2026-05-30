## ADDED Requirements

### Requirement: Evidence packaging changes advance Phase 4 without changing provider scope
The project SHALL treat retrieval evidence packs, citation policy metadata, and insufficient-evidence diagnostics as Phase 4 roadmap work when they help callers answer safely without moving final answer policy into the provider.

#### Scenario: Evidence packaging is phase-aligned
- **WHEN** an OpenSpec change adds evidence pack metadata for RAG retrieve or answer envelopes
- **THEN** the change identifies Phase 4 as the roadmap phase it advances

#### Scenario: Evidence packaging does not imply answer policy ownership
- **WHEN** the provider exposes evidence status or allowed citations
- **THEN** the roadmap boundary still states that the caller owns final user-facing answer style, refusal policy, and workflow decisions
