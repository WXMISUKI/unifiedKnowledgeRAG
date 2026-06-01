## ADDED Requirements

### Requirement: Phase 3 runtime promotion decision SHALL be explicitly recorded

The project SHALL preserve a documentation-only decision record for each Phase 3 promotion review cycle before any runtime default promotion.

#### Scenario: Decision record captures no-promotion verdict

- **WHEN** Phase 3 evidence remains candidate-level or review-level
- **THEN** the decision record states `keep_runtime_defaults` and lists open gates for production promotion

#### Scenario: Decision record remains boundary-safe

- **WHEN** the decision record is published
- **THEN** it does not change provider runtime defaults, public API contracts, GraphRAG planned boundary, or caller ownership responsibilities
