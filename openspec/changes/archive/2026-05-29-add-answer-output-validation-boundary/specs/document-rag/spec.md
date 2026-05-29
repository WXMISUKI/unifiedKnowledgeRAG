## ADDED Requirements

### Requirement: RAG answer validates cited output
The system SHALL validate cited answer output against the prompt package citation constraints before returning an answered result.

#### Scenario: Answered output passes validation
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes output validation metadata showing validation passed

#### Scenario: Answer citations are constrained
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** every returned citation is included in `result.metadata.prompt_package.allowed_citations`

#### Scenario: Invalid cited output fails closed
- **WHEN** a composer output includes citations outside the prompt package allowed citations
- **THEN** the provider treats the output as not validated and does not endorse it as an answered result
