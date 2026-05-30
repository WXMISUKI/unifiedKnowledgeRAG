## ADDED Requirements

### Requirement: Provider smoke covers insufficient-evidence evidence packs
The provider contract smoke report SHALL validate that RAG retrieval and cited answer envelopes fail closed with machine-readable evidence pack diagnostics when no supporting evidence is returned.

#### Scenario: Smoke checks insufficient-evidence retrieval pack
- **WHEN** the provider contract smoke runs against a query with no matching evidence
- **THEN** the smoke report verifies the retrieval response has `ok=true`, no documents, no allowed citations, and `result.metadata.evidence_pack.status=insufficient_evidence`

#### Scenario: Smoke checks insufficient-evidence answer pack
- **WHEN** the provider contract smoke runs the answer endpoint against the same query with no matching evidence
- **THEN** the smoke report verifies the answer response has `ok=true`, `result.answer_status=insufficient_evidence`, no answer citations, and `result.metadata.evidence_pack.reason=no_documents`

#### Scenario: Smoke report remains local and read-only
- **WHEN** insufficient-evidence pack smoke is executed
- **THEN** it does not start ingestion jobs, rebuild indexes, call embedding models, call vector databases, or execute graph queries
