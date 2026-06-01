## ADDED Requirements

### Requirement: Private-network promotion decision records SHALL be explicit before runtime promotion

The project SHALL preserve a documentation-only decision record for each Qdrant+BGE private-network promotion review cycle before any runtime default promotion.

#### Scenario: Decision record captures keep-default verdict

- **WHEN** review evidence remains `review` or has open gates
- **THEN** the decision record states `keep_runtime_defaults` and lists open gates

#### Scenario: Decision record preserves boundaries

- **WHEN** the decision record is published
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged
