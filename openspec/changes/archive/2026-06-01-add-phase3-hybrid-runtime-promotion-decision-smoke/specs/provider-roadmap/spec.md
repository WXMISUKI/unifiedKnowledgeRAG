## ADDED Requirements

### Requirement: Phase 3 hybrid runtime promotion decision smoke remains lightweight evidence maintenance

The project SHALL treat Phase 3 hybrid runtime promotion decision smoke as lightweight evidence maintenance when it validates final decision evidence-chain completeness without changing runtime defaults.

#### Scenario: Hybrid decision smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes hybrid runtime promotion decision smoke evidence
- **THEN** the roadmap records it as Phase 3 evidence maintenance and review ergonomics work

#### Scenario: Hybrid decision smoke preserves boundaries

- **WHEN** smoke checks run
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged
