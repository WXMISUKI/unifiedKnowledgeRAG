## ADDED Requirements

### Requirement: BGE-M3 quality/latency comparison contracts are Phase 6/Phase 3 bridge evidence

The project SHALL treat BGE-M3 vs mock/fixture quality and latency comparison contracts as lightweight Phase 6 deployment evidence with explicit Phase 3 promotion bridge value.

#### Scenario: Comparison contract is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a BGE-M3 quality/latency comparison contract
- **THEN** the roadmap records it as bridge evidence and not as runtime promotion

#### Scenario: Comparison contract preserves boundaries

- **WHEN** the comparison contract is reviewed
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged
