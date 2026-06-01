## ADDED Requirements

### Requirement: Deployed field-validation decision records SHALL be explicit before promotion review

The project SHALL preserve a documentation-only decision record for each Phase 6 deployed field-validation review cycle before any runtime default promotion.

#### Scenario: Decision record captures keep-default verdict

- **WHEN** deployed field-validation evidence remains review-level or has open gates
- **THEN** the decision record states `keep_local_review_until_deployed_smoke` and lists open gates

#### Scenario: Decision record preserves boundaries

- **WHEN** the decision record is published
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged
