## ADDED Requirements

### Requirement: Qdrant+BGE-M3 private-network promotion review contracts are Phase 6/Phase 3 bridge evidence

The project SHALL treat Qdrant+BGE-M3 private-network promotion review contracts as lightweight Phase 6 evidence with explicit Phase 3 promotion bridge value.

#### Scenario: Private-network review contract is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a private-network promotion review contract
- **THEN** the roadmap records it as review-governance evidence and not runtime promotion

#### Scenario: Private-network review contract preserves boundaries

- **WHEN** the contract is reviewed
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged
