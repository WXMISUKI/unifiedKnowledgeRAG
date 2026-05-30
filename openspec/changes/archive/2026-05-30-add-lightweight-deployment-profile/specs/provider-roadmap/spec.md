## ADDED Requirements

### Requirement: Phase 6 includes lightweight deployment profiles

The project SHALL treat container and compose deployment profiles as Phase 6 deployment work when they help run the provider as a component without introducing platform ownership.

#### Scenario: Deployment profile is phase-aligned

- **WHEN** an OpenSpec change adds Docker or compose deployment files for the provider component
- **THEN** the roadmap treats it as Phase 6 deployment and operations work

#### Scenario: Deployment profile preserves provider boundary

- **WHEN** a deployment profile is added
- **THEN** it does not imply ownership of TLS termination, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy
