## MODIFIED Requirements

### Requirement: Phase 3 benchmark fixtures include customer-like gate cases

The system SHALL maintain a lightweight customer-like fixture extension for retrieval benchmark evaluation so Phase 3 promotion reviews can inspect false-positive and false-negative behavior beyond baseline seed phrasing.

#### Scenario: Customer-like fixture includes false-negative review cases

- **WHEN** benchmark cases are loaded from the canonical retrieval benchmark fixture
- **THEN** customer-like additions include at least one non-empty case that targets false-negative risk in refund/logistics support workflows

#### Scenario: Customer-like fixture includes false-positive review cases

- **WHEN** benchmark cases are loaded from the canonical retrieval benchmark fixture
- **THEN** customer-like additions include at least one expected-empty case that targets lexical-overlap false-positive risk in refund/logistics support workflows
