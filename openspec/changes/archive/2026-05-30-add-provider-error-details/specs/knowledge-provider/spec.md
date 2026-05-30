## ADDED Requirements

### Requirement: Provider errors expose machine-readable details
The system SHALL include optional machine-readable details on structured provider errors without changing existing error codes or messages.

#### Scenario: Unknown RAG source error includes details
- **WHEN** a caller requests document RAG retrieval or answer with unknown knowledge base ids
- **THEN** the provider error includes `details.requested_source_ids` and `details.unknown_source_ids`

#### Scenario: Not-ready RAG index error includes details
- **WHEN** a caller requests document RAG retrieval or answer for a source whose index is not ready
- **THEN** the provider error includes `details.requested_source_ids`, `details.not_ready_source_ids`, and `details.retrieval_backend`

#### Scenario: Answer composer error includes details
- **WHEN** the configured answer composer is unsupported or not implemented
- **THEN** the provider error includes the configured composer, configured model, and supported composer names

#### Scenario: Graph query not implemented error includes details
- **WHEN** a caller requests `POST /api/graph/query` before GraphRAG execution is implemented
- **THEN** the provider error includes the requested graph id, planned status, and graph capability id

#### Scenario: Existing error envelope is preserved
- **WHEN** provider error details are added
- **THEN** existing `ok=false`, `result=null`, `error.code`, and `error.message` behavior remains compatible
