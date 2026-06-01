## MODIFIED Requirements

### Requirement: Phase 3 benchmark fixtures include customer-like gate cases

The system SHALL maintain a lightweight customer-like fixture extension for retrieval benchmark evaluation so Phase 3 promotion reviews can inspect false-positive and false-negative behavior beyond baseline seed phrasing.

#### Scenario: Customer-like fixture includes promotion-review cases

- **WHEN** benchmark cases are loaded from the canonical retrieval benchmark fixture
- **THEN** the customer-like additions include a bounded set of support-like cases that cover policy nuance phrasing, identifier noise, or expected-empty traps

#### Scenario: Customer-like fixture stays evaluation-only

- **WHEN** the benchmark fixture is refreshed after expansion
- **THEN** the generated evidence still documents evaluation-only retrieval behavior and does not change runtime defaults
