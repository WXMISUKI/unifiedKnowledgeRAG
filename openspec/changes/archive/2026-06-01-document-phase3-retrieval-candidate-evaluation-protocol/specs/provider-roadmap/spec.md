## ADDED Requirements

### Requirement: Phase 3 candidate evaluation protocols stay lightweight and review-only

The project SHALL treat Phase 3 retrieval candidate evaluation protocols as lightweight evidence-governance work when they standardize gate review expectations without changing runtime defaults.

#### Scenario: Protocol document is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 retrieval candidate evaluation protocol
- **THEN** the roadmap records it as Phase 3 evidence-governance work rather than retrieval runtime promotion

#### Scenario: Protocol document preserves provider boundaries

- **WHEN** the protocol defines gate expectations for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, or relation-aware grading
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG execution boundaries, and caller ownership remain unchanged until separate evidence-backed promotion changes are approved
