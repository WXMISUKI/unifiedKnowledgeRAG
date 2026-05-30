## ADDED Requirements

### Requirement: Deployed provider smoke advances Phase 6 operations

The project SHALL treat deployed provider HTTP smoke evidence as Phase 6 deployment and operations work when it helps verify an already-running provider component before external binding.

#### Scenario: Deployed smoke is phase-aligned

- **WHEN** an OpenSpec change adds a deployed HTTP smoke probe for provider discovery and handoff endpoints
- **THEN** the roadmap treats it as Phase 6 deployment and operations evidence rather than retrieval, GraphRAG, or platform-control work

#### Scenario: Deployed smoke preserves provider boundary

- **WHEN** deployed provider smoke evidence is exported
- **THEN** it does not imply ownership of TLS termination, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy
