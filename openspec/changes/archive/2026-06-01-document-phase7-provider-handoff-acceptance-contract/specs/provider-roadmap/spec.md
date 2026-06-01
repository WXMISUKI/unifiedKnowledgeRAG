## ADDED Requirements

### Requirement: Phase 7 handoff acceptance contract remains evidence-only and boundary-safe

The project SHALL allow a Phase 7 provider handoff acceptance contract that defines cross-phase acceptance semantics without changing runtime defaults.

#### Scenario: Contract clarifies cross-phase handoff semantics

- **WHEN** the acceptance contract is reviewed
- **THEN** it distinguishes required evidence, optional review evidence, and the meaning of `ready/review/blocked` for handoff consumers

#### Scenario: Contract preserves promotion and ownership boundaries

- **WHEN** the acceptance contract is added or updated
- **THEN** runtime default promotion remains separately gated and caller control-plane ownership remains unchanged
