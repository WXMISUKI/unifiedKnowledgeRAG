## ADDED Requirements

### Requirement: Phase 3 aggregation and relation-aware negative-control smoke stays lightweight and evaluation-only

The project SHALL treat the Phase 3 aggregation/relation negative-control smoke as lightweight evidence visibility work when it summarizes over-broad aggregation risk and relation-aware grading alignment without changing runtime defaults.

#### Scenario: Negative-control smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 aggregation/relation negative-control smoke
- **THEN** the roadmap records it as Phase 3 evidence maintenance work rather than runtime promotion

#### Scenario: Negative-control smoke preserves runtime defaults

- **WHEN** the smoke validates positive and negative aggregation controls plus relation-aware grading alignment
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged
