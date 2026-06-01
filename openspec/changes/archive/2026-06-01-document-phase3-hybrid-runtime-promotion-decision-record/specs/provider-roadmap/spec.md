## ADDED Requirements

### Requirement: Phase 3 hybrid runtime promotion decision SHALL be explicitly recorded

The project SHALL preserve a documentation-only final decision record for each Phase 3 hybrid runtime promotion review cycle before any runtime default promotion.

#### Scenario: Hybrid decision record captures keep-default verdict

- **WHEN** hybrid promotion evidence remains candidate-level or review-level
- **THEN** the decision record states `keep_runtime_defaults` and lists open gates for production promotion

#### Scenario: Hybrid decision record remains boundary-safe

- **WHEN** the hybrid decision record is published
- **THEN** it does not change provider runtime defaults, public API contracts, GraphRAG planned boundary, or caller ownership responsibilities
