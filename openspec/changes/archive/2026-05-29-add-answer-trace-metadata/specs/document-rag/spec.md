## ADDED Requirements

### Requirement: RAG answer exposes machine-readable answer trace metadata
The system SHALL include a compact machine-readable answer trace in document RAG answer metadata for successful answer envelopes.

#### Scenario: Answered result includes answer trace
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=answered`
- **THEN** `result.metadata.answer_trace` includes a trace id, trace version, final status, and ordered stages for retrieval, evidence gate, composer, output parser, output validator, and final decision

#### Scenario: Evidence gate failure includes answer trace
- **WHEN** `POST /api/rag/answer` returns `result.answer_status=insufficient_evidence` because the evidence gate failed
- **THEN** `result.metadata.answer_trace` includes retrieval, evidence gate, composer, and final decision stages without prompt text or raw generated output

#### Scenario: Finalizer validation failure includes answer trace
- **WHEN** the shared finalization pipeline rejects a composer candidate because citations are missing or invalid
- **THEN** `result.metadata.answer_trace` includes output parser, output validator, and final decision stages that explain the fail-closed decision

#### Scenario: Answer trace preserves existing answer contract
- **WHEN** answer trace metadata is added
- **THEN** the existing answer, citations, documents, prompt package, prompt render, output parser, and output validation metadata remain compatible
