## ADDED Requirements

### Requirement: BGE-M3 artifact readiness is treated as Phase 6 bridge evidence

The project SHALL treat BGE-M3 artifact readiness as lightweight deployment evidence that supports Phase 3 promotion review without changing runtime defaults.

#### Scenario: Artifact readiness is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes BGE-M3 artifact readiness evidence
- **THEN** the roadmap records it as Phase 6 deployment evidence with Phase 3 bridge value

#### Scenario: Artifact readiness preserves boundaries

- **WHEN** the readiness report summarizes checksum-aware model artifact state
- **THEN** runtime embedding defaults, provider HTTP contracts, and promotion decisions remain unchanged
