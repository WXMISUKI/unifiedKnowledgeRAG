## ADDED Requirements

### Requirement: Phase 6 handoff evidence may be exposed through read-only HTTP discovery

The project SHALL allow Phase 6 integration and operations evidence to be exposed through lightweight read-only HTTP discovery when it helps external control planes bind the provider without taking over provider internals.

#### Scenario: Handoff API remains phase-aligned

- **WHEN** an OpenSpec change exposes existing handoff evidence through a read-only HTTP endpoint
- **THEN** the roadmap treats it as Phase 6 integration evidence rather than a runtime retrieval, GraphRAG, or platform-control feature

#### Scenario: Handoff API preserves provider boundary

- **WHEN** the provider exposes handoff evidence over HTTP
- **THEN** external control planes still own registration, heartbeat governance, audit policy, source-to-agent binding decisions, and final answer policy
