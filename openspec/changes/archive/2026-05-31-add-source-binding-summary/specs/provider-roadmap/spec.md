## ADDED Requirements

### Requirement: Source binding summary bridges Phase 2 and Phase 6

The project SHALL treat source binding summary evidence as a lightweight bridge between Phase 2 document ingestion diagnostics and Phase 6 provider integration operations.

#### Scenario: Source binding summary is phase-aligned

- **WHEN** an OpenSpec change adds a read-only summary of source bindability for external control planes
- **THEN** the roadmap treats it as Phase 2 and Phase 6 work rather than source-to-agent control-plane ownership

#### Scenario: Source binding summary preserves provider boundary

- **WHEN** the provider reports source bindability facts and recommended actions
- **THEN** MyPrivateAgent or another external control plane still owns source-to-agent binding decisions, policy, approvals, audit, and final answer workflow
