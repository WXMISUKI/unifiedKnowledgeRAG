# approved-local-corpus-acceptance-smoke Specification

## Purpose
TBD - created by archiving change add-approved-local-corpus-acceptance-smoke. Update Purpose after archive.
## Requirements
### Requirement: Approved local corpus acceptance smoke can be exported
The system SHALL export a local acceptance smoke report for an approved local corpus source.

#### Scenario: Approved corpus passes acceptance
- **WHEN** the approved source is visible in provider catalog and answerable business questions return evidence with valid citations
- **THEN** the report has `decision=go`
- **AND** it records case-level retrieve counts, answer statuses, citations, and invalid citation counts

#### Scenario: Approved corpus needs review
- **WHEN** the approved source is visible but one or more expected-answerable questions return weak or missing evidence
- **THEN** the report has `decision=review`
- **AND** it recommends reviewing the corpus content, page range, or query set

#### Scenario: Approved corpus is blocked
- **WHEN** the source is not registered, the manifest fails, retrieve/answer contract fails, or an answer cites outside the retrieved evidence allowlist
- **THEN** the report has `decision=blocked`
- **AND** it records the blocking reason

### Requirement: Acceptance smoke includes negative-control behavior
The acceptance smoke SHALL include unrelated negative-control queries so local corpus acceptance does not rely only on positive matches.

#### Scenario: Unrelated query is tested
- **WHEN** the smoke runs an unrelated query against the approved local corpus
- **THEN** the case expects insufficient evidence or no returned documents
- **AND** any citation returned for that negative-control case marks the case as review or blocked according to citation validity

### Requirement: Acceptance smoke remains lightweight
The approved local corpus acceptance smoke SHALL validate existing local provider behavior without mutating runtime state.

#### Scenario: Acceptance smoke runs
- **WHEN** the smoke command runs
- **THEN** it does not register sources, create source-to-agent bindings, create formal ingestion jobs, start OCR services, promote retrieval backends, run MyPrivateAgent orchestration, call vector databases, or execute GraphRAG

