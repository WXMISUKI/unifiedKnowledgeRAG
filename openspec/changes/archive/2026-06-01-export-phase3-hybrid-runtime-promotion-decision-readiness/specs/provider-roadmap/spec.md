## ADDED Requirements

### Requirement: Phase 3 hybrid runtime promotion decision readiness exports stay lightweight and review-only

The project SHALL treat hybrid runtime promotion decision readiness exports as local Phase 3 evidence visibility work without changing runtime defaults.

#### Scenario: Hybrid decision readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes hybrid runtime promotion decision readiness evidence
- **THEN** the roadmap records it as Phase 3 review visibility and not runtime promotion

#### Scenario: Hybrid decision readiness export preserves boundaries

- **WHEN** the export summarizes review signals and open gates
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG planned boundaries, and caller ownership remain unchanged
