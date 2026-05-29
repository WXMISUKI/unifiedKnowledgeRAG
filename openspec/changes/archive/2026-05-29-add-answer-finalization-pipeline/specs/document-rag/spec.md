## ADDED Requirements

### Requirement: RAG answer uses shared finalization pipeline
The system SHALL finalize cited answer candidates through a shared provider-owned pipeline before returning an answered result.

#### Scenario: Valid candidate is finalized as answered
- **WHEN** a composer candidate answer text contains allowed citations
- **THEN** the finalization pipeline returns an answered result with prompt package, prompt render, output parser, and output validation metadata

#### Scenario: Invalid candidate fails closed
- **WHEN** a composer candidate answer text contains no citations or citations outside the allowed prompt package citations
- **THEN** the finalization pipeline returns an insufficient-evidence result rather than an answered result

#### Scenario: Public answer contract is preserved
- **WHEN** deterministic answer composition uses the shared finalization pipeline
- **THEN** the public `POST /api/rag/answer` response remains compatible with the existing cited answer envelope
