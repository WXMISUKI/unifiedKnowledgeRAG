## ADDED Requirements

### Requirement: Evidence provenance advances Phase 4 packaging

The project SHALL treat provider-owned evidence provenance as Phase 4 evidence packaging work when it helps callers answer from returned citations without moving final answer policy into the provider.

#### Scenario: Evidence provenance is phase-aligned

- **WHEN** an OpenSpec change adds provenance metadata to evidence packs
- **THEN** the roadmap records it as Phase 4 evidence packaging work

#### Scenario: Evidence provenance preserves caller ownership

- **WHEN** evidence packs include source path, chunk id, chunking strategy, and citation anchor metadata
- **THEN** the caller still owns final response style, refusal policy, approval workflow, and final orchestration
