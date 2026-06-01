## ADDED Requirements

### Requirement: Phase 6 Qdrant+BGE-M3 private-network promotion readiness exports stay lightweight and review-only

The project SHALL treat Qdrant+BGE-M3 private-network promotion readiness exports as local evidence visibility work without changing runtime defaults.

#### Scenario: Private-network readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes private-network promotion readiness export evidence
- **THEN** the roadmap records it as Phase 6 bridge visibility and not runtime promotion

#### Scenario: Private-network readiness export preserves boundaries

- **WHEN** the export summarizes review gates and open evidence inputs
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged
