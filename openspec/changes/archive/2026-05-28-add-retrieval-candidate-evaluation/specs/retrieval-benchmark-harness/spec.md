## ADDED Requirements

### Requirement: Retrieval candidates can be evaluated consistently

The system SHALL run the same retrieval benchmark cases against one or more named retrieval candidates.

#### Scenario: Candidate has evaluation metadata

- **WHEN** a retrieval candidate is defined
- **THEN** it includes a stable id, backend, description, and optional metadata for later architecture review

#### Scenario: Multiple candidates are evaluated

- **WHEN** multiple retrieval candidates are evaluated together
- **THEN** each candidate is run against the same benchmark cases and returns its own benchmark report

#### Scenario: Candidate IDs are validated

- **WHEN** candidate evaluation is requested
- **THEN** duplicate or filesystem-unsafe candidate ids are rejected before benchmark execution

### Requirement: Retrieval candidate evidence can be exported

The system SHALL export per-candidate benchmark evidence using stable candidate-based filenames.

#### Scenario: Candidate report files are exported

- **WHEN** candidate evaluation is run with an output directory
- **THEN** each candidate writes `<candidate-id>.json` and `<candidate-id>.md` benchmark reports

#### Scenario: Candidate export remains local

- **WHEN** candidate evaluation exports evidence
- **THEN** it writes local files without exposing a new public HTTP API
