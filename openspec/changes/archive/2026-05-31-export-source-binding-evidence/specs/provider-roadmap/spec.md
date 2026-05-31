## ADDED Requirements

### Requirement: Source binding evidence participates in Phase 6 handoff

The project SHALL include source binding evidence in Phase 6 handoff artifacts when it helps external control planes review source readiness without moving binding policy into the provider.

#### Scenario: Source binding evidence is phase-aligned

- **WHEN** an OpenSpec change exports source binding summary evidence and adds it to handoff refresh
- **THEN** the roadmap treats it as Phase 2/6 evidence work

#### Scenario: Source binding evidence preserves provider boundary

- **WHEN** source binding evidence is included in the handoff bundle
- **THEN** MyPrivateAgent or another external control plane still owns source-to-agent binding decisions, policy, approvals, audit, and final answer workflow
