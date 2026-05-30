## ADDED Requirements

### Requirement: RAG retrieval exposes provider evidence pack metadata
The system SHALL include a compact provider-owned evidence pack in successful document RAG retrieval metadata so callers can compose answers from allowed citations without inferring the citation policy from raw documents.

#### Scenario: Retrieval with evidence includes evidence pack
- **WHEN** `POST /api/rag/retrieve` returns `ok=true` with retrieved documents
- **THEN** `result.metadata.evidence_pack` includes pack id, version `evidence-pack-v1`, status `answerable`, citation policy, allowed citations, evidence count, score summary, retrieval backend, requested source ids, and compact evidence entries

#### Scenario: Evidence pack citations match returned documents
- **WHEN** `POST /api/rag/retrieve` returns an evidence pack
- **THEN** every allowed citation in the pack corresponds to a citation in `result.documents`

#### Scenario: Empty retrieval includes insufficient evidence pack
- **WHEN** `POST /api/rag/retrieve` returns `ok=true` with no retrieved documents
- **THEN** `result.metadata.evidence_pack` has status `insufficient_evidence`, reason `no_documents`, zero evidence count, and no allowed citations

### Requirement: RAG answer reuses retrieval evidence pack metadata
The system SHALL include the same retrieval-owned evidence pack metadata in successful document RAG answer envelopes before answer-specific prompt or validation metadata is considered.

#### Scenario: Answered result includes evidence pack
- **WHEN** `POST /api/rag/answer` returns `ok=true` with `result.answer_status=answered`
- **THEN** `result.metadata.evidence_pack` is present and its allowed citations include every returned answer citation

#### Scenario: Insufficient answer includes diagnostic evidence pack
- **WHEN** `POST /api/rag/answer` returns `ok=true` with `result.answer_status=insufficient_evidence`
- **THEN** `result.metadata.evidence_pack` remains present for diagnostics and does not expose unsupported citations as endorsed answer citations

#### Scenario: Evidence pack preserves existing contracts
- **WHEN** evidence pack metadata is added to retrieval and answer responses
- **THEN** existing answer context, documents, retrieval trace, answer trace, prompt package, prompt render, output parser, and output validation metadata remain compatible
