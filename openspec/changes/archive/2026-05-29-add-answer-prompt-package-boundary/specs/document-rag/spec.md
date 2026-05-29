## ADDED Requirements

### Requirement: RAG answer builds a cited prompt package
The system SHALL build a provider-owned cited-answer prompt package from the user query and gated retrieval evidence before composing an answered result.

#### Scenario: Answered result includes prompt package metadata
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata` includes a prompt package id, citation policy, and allowed citations derived from the supporting evidence

#### Scenario: Prompt package citations match answer citations
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** the prompt package allowed citations match `result.citations`

#### Scenario: Insufficient evidence has no endorsed prompt package
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=insufficient_evidence`
- **THEN** the result does not expose endorsed prompt package metadata
