## ADDED Requirements

### Requirement: RAG answer renders cited prompt packages
The system SHALL render cited-answer prompt packages into provider-owned model-ready message structures before composing an answered result.

#### Scenario: Answered result includes prompt render metadata
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes prompt render metadata with renderer id and message count

#### Scenario: Render metadata aligns with prompt package
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** the prompt render metadata references the same prompt package id as `result.metadata.prompt_package.id`

#### Scenario: Insufficient evidence has no endorsed prompt render
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=insufficient_evidence`
- **THEN** the result does not expose endorsed prompt render metadata
