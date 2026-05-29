## ADDED Requirements

### Requirement: RAG answer applies configurable evidence sufficiency policy
The system SHALL evaluate retrieved evidence against configurable answer sufficiency settings before returning an answered cited response.

#### Scenario: Evidence passes sufficiency policy
- **WHEN** a caller requests `POST /api/rag/answer` and retrieved documents satisfy the configured minimum evidence count and minimum top evidence score
- **THEN** the response has `ok=true`, `result.answer_status=answered`, non-empty `result.answer`, and metadata describing the sufficiency policy

#### Scenario: Evidence fails minimum top score
- **WHEN** a caller requests `POST /api/rag/answer` and retrieved documents do not satisfy the configured minimum top evidence score
- **THEN** the response has `ok=true`, `result.answer_status=insufficient_evidence`, an empty `result.answer`, empty `result.citations`, and metadata describing the failed gate

#### Scenario: Evidence fails minimum count
- **WHEN** a caller requests `POST /api/rag/answer` and retrieved documents do not satisfy the configured minimum evidence count
- **THEN** the response has `ok=true`, `result.answer_status=insufficient_evidence`, an empty `result.answer`, empty `result.citations`, and metadata describing the failed gate

#### Scenario: Retrieved evidence remains inspectable after gate failure
- **WHEN** the answer endpoint refuses to answer because retrieved evidence fails the sufficiency policy
- **THEN** the response keeps the retrieved `result.documents` for diagnostics without endorsing them as answer citations
