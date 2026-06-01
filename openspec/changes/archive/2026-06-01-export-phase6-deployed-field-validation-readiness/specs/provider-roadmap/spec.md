## ADDED Requirements

### Requirement: Phase 6 deployed field validation readiness exports stay lightweight and review-only

The project SHALL treat deployed field validation readiness exports as local Phase 6 evidence visibility work without changing runtime defaults.

#### Scenario: Deployed field validation readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes deployed field validation readiness evidence
- **THEN** the roadmap records it as Phase 6 operations evidence visibility work rather than runtime promotion

#### Scenario: Deployed field validation readiness export preserves boundaries

- **WHEN** the export summarizes deployment readiness, handoff bundle posture, and deployed smoke evidence
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged
