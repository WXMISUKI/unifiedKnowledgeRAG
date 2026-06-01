## ADDED Requirements

### Requirement: Phase 3 hybrid runtime promotion decision review SHALL have a dedicated contract

The project SHALL maintain a documentation-only contract for the final Phase 3 hybrid runtime promotion review before any runtime default switch is considered.

#### Scenario: Hybrid decision contract is phase-aligned and evidence-driven

- **WHEN** a reviewer evaluates whether hybrid runtime defaults can be promoted
- **THEN** the contract lists required Phase 3 and Phase 6 bridge evidence inputs and explicit review-state semantics

#### Scenario: Hybrid decision contract preserves provider boundaries

- **WHEN** the contract is published or refreshed
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG planned boundaries, and caller control-plane ownership remain unchanged
