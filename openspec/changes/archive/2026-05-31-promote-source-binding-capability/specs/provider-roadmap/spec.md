## ADDED Requirements

### Requirement: Source binding capability promotion advances Phase 6 integration

The project SHALL treat source binding review capability promotion as Phase 6 integration work when it helps external control planes discover provider-owned binding evidence without making the provider a policy engine.

#### Scenario: Source binding capability is phase-aligned

- **WHEN** an OpenSpec change promotes source binding summary to a formal provider capability
- **THEN** the roadmap records it as lightweight Phase 6 integration work

#### Scenario: Source binding capability preserves external ownership

- **WHEN** source binding review is discoverable through provider capabilities
- **THEN** source-to-agent binding policy, approvals, audit, and execution remain owned by MyPrivateAgent or another external control plane
