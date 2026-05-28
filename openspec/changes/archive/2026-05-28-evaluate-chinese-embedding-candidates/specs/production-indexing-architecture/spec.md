## ADDED Requirements

### Requirement: Chinese embedding candidates are evaluated before approval

The system SHALL evaluate Chinese-heavy embedding candidates as explicit architecture candidates before approving a production embedding provider.

#### Scenario: Candidate metadata is recorded

- **WHEN** an embedding candidate is defined for evaluation
- **THEN** it records stable id, provider family, model name, deployment mode, language profile, vector dimension, data residency posture, operational complexity, reranker compatibility, and approval status

#### Scenario: Candidate remains unapproved

- **WHEN** an embedding candidate is included in the evaluation catalog
- **THEN** the system treats it as evidence for review and does not enable hosted or local embedding calls by default

#### Scenario: Chinese-heavy workload is evaluated

- **WHEN** the project evaluates an embedding model for the expected workload
- **THEN** the evaluation states whether the candidate is suitable for Chinese-heavy corpora and whether it supports private-network deployment
