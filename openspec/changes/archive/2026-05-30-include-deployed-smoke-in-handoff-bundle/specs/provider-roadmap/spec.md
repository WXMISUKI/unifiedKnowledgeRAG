## ADDED Requirements

### Requirement: Handoff evidence may include optional deployed smoke

The project SHALL allow Phase 6 provider handoff evidence to include optional deployed smoke status so external control planes can review live deployment reachability without making local development depend on a deployed URL.

#### Scenario: Optional deployed smoke is phase-aligned

- **WHEN** an OpenSpec change adds deployed smoke evidence to the provider handoff bundle
- **THEN** the roadmap treats it as Phase 6 integration and operations evidence

#### Scenario: Optional deployed smoke preserves provider boundary

- **WHEN** deployed smoke is summarized in handoff evidence
- **THEN** it does not imply ownership of provider registration, heartbeat governance, audit policy, TLS termination, reverse proxy policy, managed secrets, source-to-agent binding, or final answer policy
