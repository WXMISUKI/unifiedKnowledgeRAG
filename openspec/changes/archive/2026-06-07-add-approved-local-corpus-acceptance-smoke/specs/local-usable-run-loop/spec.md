## ADDED Requirements

### Requirement: Local usability can include approved corpus acceptance context
The local usability workflow SHALL allow a registered local corpus acceptance smoke to provide corpus-specific readiness context without replacing the generic provider run-loop.

#### Scenario: Approved corpus acceptance is available
- **WHEN** the approved local corpus acceptance smoke has been exported
- **THEN** local usability review can use its `go`, `review`, or `blocked` decision as corpus-specific evidence

#### Scenario: Generic run-loop remains separate
- **WHEN** the approved corpus acceptance smoke is added
- **THEN** the generic local usable run-loop continues to validate provider discovery, preflight, retrieve, and answer over its configured source and query
