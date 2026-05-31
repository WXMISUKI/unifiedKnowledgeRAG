## ADDED Requirements

### Requirement: Deployment readiness guidance includes a configuration reference

The project SHALL provide a deployment configuration reference that maps runtime environment variables, mount points, and evidence refresh commands to the current deployment readiness state.

#### Scenario: Operators can identify deployment inputs

- **WHEN** an operator reviews deployment readiness guidance
- **THEN** the configuration reference shows which environment variables and mounted paths are relevant for deployment preparation

#### Scenario: Configuration reference remains documentation-only

- **WHEN** the configuration reference is published
- **THEN** it does not change runtime defaults, deployment automation, or provider governance boundaries
