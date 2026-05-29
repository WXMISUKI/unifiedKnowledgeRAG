## ADDED Requirements

### Requirement: RAG answer returns cited answer envelopes
The system SHALL expose a document RAG answer endpoint that composes a provider-owned answer envelope from configured retrieval evidence without changing the existing retrieval endpoint contract.

#### Scenario: Answer is composed from retrieved evidence
- **WHEN** a caller requests `POST /api/rag/answer` with a valid query and ready knowledge base id whose retrieval returns evidence
- **THEN** the response has `ok=true`, `result.answer_status=answered`, non-empty `result.answer`, non-empty `result.citations`, and the supporting `result.documents`

#### Scenario: Answer citations match supporting evidence
- **WHEN** the answer endpoint returns an answered result
- **THEN** every citation in `result.citations` corresponds to a citation in `result.documents`

#### Scenario: Retrieval endpoint remains unchanged
- **WHEN** the cited answer endpoint is added
- **THEN** `POST /api/rag/retrieve` continues to return the existing retrieval envelope with `answer_context` and `documents`

### Requirement: RAG answer fails closed when evidence is insufficient
The system SHALL return a successful answer envelope with an explicit insufficient-evidence status when retrieval produces no usable evidence.

#### Scenario: Retrieval has no evidence
- **WHEN** a caller requests `POST /api/rag/answer` with a valid query and ready knowledge base id whose retrieval returns no documents
- **THEN** the response has `ok=true`, `result.answer_status=insufficient_evidence`, an empty `result.answer`, an empty `result.citations`, and an empty `result.documents`

#### Scenario: Insufficient evidence is not a provider error
- **WHEN** the answer endpoint cannot answer because indexed evidence is insufficient
- **THEN** the response does not use `error` and instead reports the insufficiency in `result.answer_status`

### Requirement: RAG answer preserves retrieval guardrails
The system SHALL enforce existing source validation and index readiness checks before answer orchestration performs backend retrieval work.

#### Scenario: Unknown source is requested for answer
- **WHEN** a caller requests `POST /api/rag/answer` with an unknown knowledge base id
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source

#### Scenario: Not-ready source is requested for answer
- **WHEN** a caller requests `POST /api/rag/answer` for a known source whose index status is not ready
- **THEN** the response has `ok=false` and an `error.code` that identifies the index readiness failure
