## ADDED Requirements

### Requirement: RAG evidence pack consumption remains caller-owned
The system SHALL keep evidence pack consumption rules explicit so callers can treat the pack as trusted evidence without moving final answer policy into the provider.

#### Scenario: Answerable pack exposes a caller allowlist
- **WHEN** `POST /api/rag/retrieve` or `POST /api/rag/answer` returns `result.metadata.evidence_pack.status=answerable`
- **THEN** the caller can treat `allowed_citations` as the authoritative allowlist for composing or validating a cited answer

#### Scenario: Diagnostic fields remain diagnostic
- **WHEN** a caller inspects `pack_id`, `score_summary`, `retrieval_backend`, `requested_source_ids`, or `filter_context`
- **THEN** those fields are treated as diagnostic evidence and not as a separate answer-policy authority

#### Scenario: Insufficient evidence remains fail-closed
- **WHEN** `result.metadata.evidence_pack.status=insufficient_evidence`
- **THEN** the caller does not infer any supported citation policy from raw documents and keeps the no-answer branch caller-owned

#### Scenario: Evidence pack consumption preserves answer compatibility
- **WHEN** the provider includes evidence pack metadata in retrieval and answer responses
- **THEN** the existing answer context, documents, retrieval trace, answer trace, prompt package, prompt render, output parser, and output validation metadata remain compatible
