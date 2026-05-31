## ADDED Requirements

### Requirement: Liveness and readiness probes advance Phase 6 high availability

The project SHALL treat liveness/readiness probe separation as Phase 6 deployment and operations work when it improves component availability without adding platform ownership.

#### Scenario: Probe split is phase-aligned

- **WHEN** an OpenSpec change adds separate liveness and readiness probes
- **THEN** the roadmap records it as lightweight Phase 6 high-availability work

#### Scenario: Probe split preserves provider boundary

- **WHEN** liveness and readiness probes are exposed
- **THEN** the provider still does not own orchestration, alert routing, autoscaling policy, registration, heartbeat governance, audit policy, or final answer workflow
