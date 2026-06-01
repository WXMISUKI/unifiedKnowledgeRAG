## ADDED Requirements

### Requirement: Deployed field-validation consistency smoke SHALL be explicit before promotion review

The project SHALL preserve a documentation-only deployed handoff consistency smoke for each Phase 6 field-validation review cycle before any runtime default promotion.

#### Scenario: Consistency smoke captures keep-default posture

- **WHEN** deployed field-validation evidence remains review-level or has open gates
- **THEN** the consistency smoke states that the local artifacts remain aligned without changing runtime defaults

#### Scenario: Consistency smoke preserves boundaries

- **WHEN** the consistency smoke is published
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged
