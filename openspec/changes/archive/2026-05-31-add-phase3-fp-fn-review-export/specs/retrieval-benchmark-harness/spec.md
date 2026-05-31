## MODIFIED Requirements

### Requirement: Retrieval benchmark reports can be exported

The system SHALL export retrieval benchmark reports as durable local evidence files.

#### Scenario: Phase 3 FP/FN review can be exported from benchmark evidence

- **WHEN** a caller exports Phase 3 FP/FN review from an existing benchmark evidence JSON
- **THEN** the system writes local JSON and Markdown files containing false-positive and false-negative counts, rates, and case ids

#### Scenario: FP/FN review export remains local and evaluation-only

- **WHEN** Phase 3 FP/FN review evidence is exported
- **THEN** runtime retrieval defaults, provider HTTP contracts, and production promotion status remain unchanged
