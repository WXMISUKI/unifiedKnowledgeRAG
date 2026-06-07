## ADDED Requirements

### Requirement: Parser-derived corpus retrieval quality baseline can be exported
The system SHALL export a local retrieval quality baseline for an approved parser-derived corpus source.

#### Scenario: Quality baseline passes
- **WHEN** the parser-derived source is visible and ready
- **AND** every answerable case returns the expected source and expected citation
- **AND** every expected-empty case returns no evidence and no endorsed answer citations
- **AND** invalid citation count is zero
- **THEN** the quality baseline report has `decision=go`
- **AND** it records source id, case count, hit rate, citation match rate, empty handling rate, invalid citation count, per-case results, and recommended next action

#### Scenario: Quality baseline needs review
- **WHEN** the parser-derived source is ready
- **AND** at least one answerable case misses expected evidence, one expected-empty case returns evidence, or one citation does not match the expected citation
- **THEN** the quality baseline report has `decision=review`
- **AND** it records the review case ids and machine-readable reason code

#### Scenario: Quality baseline is blocked
- **WHEN** the parser-derived source is not visible, its manifest is unavailable, or the RAG retrieve/answer contract fails
- **THEN** the quality baseline report has `decision=blocked`
- **AND** it records the blocking source readiness or contract reason code

### Requirement: Parser-derived corpus quality cases remain lightweight
The parser-derived corpus quality baseline SHALL use a small local case set that includes both answerable business questions and expected-empty negative controls.

#### Scenario: Case fixture is loaded
- **WHEN** the quality baseline loads its case fixture
- **THEN** each case includes case id, query, expected mode, expected source id, expected citation when answerable, category, and description

#### Scenario: Expected-empty case is defined
- **WHEN** a case is marked expected-empty
- **THEN** it has no expected citation
- **AND** successful handling requires no retrieved documents and no endorsed answer citations

### Requirement: Parser-derived corpus quality baseline remains evaluation-only
The parser-derived corpus quality baseline SHALL not change runtime retrieval behavior or promote candidate backends.

#### Scenario: Baseline runs
- **WHEN** the quality baseline command runs
- **THEN** it does not parse raw PDFs
- **AND** it does not start OCR services
- **AND** it does not create ingestion jobs
- **AND** it does not call MyPrivateAgent
- **AND** it does not create source-to-agent bindings
- **AND** it does not mutate `/api/chat`
- **AND** it does not promote Qdrant, pgvector, BGE-M3, hybrid search, rerankers, or chunking defaults
- **AND** it does not execute GraphRAG
