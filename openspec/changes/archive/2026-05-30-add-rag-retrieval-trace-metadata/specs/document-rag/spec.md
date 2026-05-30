## ADDED Requirements

### Requirement: RAG retrieval exposes machine-readable retrieval trace metadata
The system SHALL include compact retrieval trace metadata in successful document RAG retrieval and answer envelopes.

#### Scenario: Retrieval result includes retrieval trace
- **WHEN** `POST /api/rag/retrieve` returns `ok=true`
- **THEN** `result.metadata.retrieval_trace` includes trace id, trace version, retrieval backend, requested source ids, top-k, document count, citations, score summary, and filter context metadata

#### Scenario: Empty retrieval includes retrieval trace
- **WHEN** `POST /api/rag/retrieve` returns an empty successful result
- **THEN** `result.metadata.retrieval_trace.document_count` is zero and citations are empty

#### Scenario: Answer result includes retrieval trace
- **WHEN** `POST /api/rag/answer` returns a successful answer envelope
- **THEN** `result.metadata.retrieval_trace` is present alongside answer metadata so retrieval and answer decisions can be correlated

#### Scenario: Retrieval trace preserves existing contracts
- **WHEN** retrieval trace metadata is added
- **THEN** existing retrieval documents, answer context, answer trace, and request filter context fields remain compatible
