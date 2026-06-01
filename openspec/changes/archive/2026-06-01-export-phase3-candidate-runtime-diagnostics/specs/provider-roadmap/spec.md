## ADDED Requirements

### Requirement: Phase 3 runtime diagnostics exports stay lightweight and evaluation-only

The project SHALL treat Phase 3 candidate runtime diagnostics exports as lightweight evidence visibility work when they summarize promotion prerequisites without changing runtime defaults.

#### Scenario: Runtime diagnostics export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 candidate runtime diagnostics export
- **THEN** the roadmap records it as Phase 3 evidence visibility work rather than runtime promotion

#### Scenario: Runtime diagnostics export preserves boundaries

- **WHEN** runtime diagnostics summarize retrieval backend, embedding provider, artifact status, and deployment-evidence presence
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged
