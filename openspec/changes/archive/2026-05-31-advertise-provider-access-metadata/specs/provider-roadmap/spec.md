## ADDED Requirements

### Requirement: Access metadata advances Phase 6 integration

The project SHALL treat machine-readable provider access metadata as Phase 6 integration work when it helps external control planes connect to the provider component without taking over identity or policy ownership.

#### Scenario: Access metadata is phase-aligned

- **WHEN** an OpenSpec change adds component access metadata to the provider manifest
- **THEN** the roadmap treats it as Phase 6 integration evidence

#### Scenario: Access metadata preserves provider boundary

- **WHEN** the provider advertises accepted component access headers
- **THEN** MyPrivateAgent or another external control plane still owns user identity, roles, approvals, audit policy, source-to-agent binding, and final answer workflow
