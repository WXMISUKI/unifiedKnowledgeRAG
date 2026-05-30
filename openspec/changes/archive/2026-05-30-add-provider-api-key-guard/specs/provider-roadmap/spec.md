## ADDED Requirements

### Requirement: Phase 6 may include lightweight component access guards

The project SHALL allow lightweight component access controls as Phase 6 deployment work when they protect provider HTTP APIs without moving external control-plane policy ownership into the provider.

#### Scenario: Access guard is phase-aligned

- **WHEN** an OpenSpec change adds an optional provider API token gate
- **THEN** the roadmap treats it as Phase 6 deployment and operations work

#### Scenario: Access guard preserves provider boundary

- **WHEN** provider API token protection is enabled
- **THEN** MyPrivateAgent or another caller still owns user identity, roles, approvals, audit policy, source-to-agent binding, and final answer policy
