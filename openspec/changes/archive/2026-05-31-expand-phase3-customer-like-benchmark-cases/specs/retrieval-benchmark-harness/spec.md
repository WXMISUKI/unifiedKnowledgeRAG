## ADDED Requirements

### Requirement: Phase 3 benchmark fixtures include customer-like gate cases

The system SHALL maintain a lightweight customer-like fixture extension for retrieval benchmark evaluation so Phase 3 promotion reviews can inspect false-positive and false-negative behavior beyond baseline seed phrasing.

#### Scenario: Customer-like fixture cases are loadable

- **WHEN** benchmark cases are loaded from the canonical retrieval benchmark fixture
- **THEN** the fixture includes additional customer-like cases with stable ids, categories, and expected outcomes

#### Scenario: Customer-like fixture cases remain evaluation-only

- **WHEN** customer-like benchmark cases are added
- **THEN** runtime retrieval defaults and provider HTTP contracts remain unchanged until separate gate evidence approves promotion

#### Scenario: Category summaries include customer-like cases

- **WHEN** benchmark evaluation runs over the updated fixture
- **THEN** summary totals and category-level metrics include the added customer-like cases
