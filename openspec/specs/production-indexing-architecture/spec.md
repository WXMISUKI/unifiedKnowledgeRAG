# production-indexing-architecture Specification

## Purpose
Defines decision gates and evaluation requirements for production-grade indexing infrastructure choices.

## Requirements
### Requirement: Production indexing choices are decision-gated

The system SHALL require an explicit architecture decision record and retrieval benchmark evidence before adding production embedding, vector store, queue worker, reranker, or graph storage dependencies.

#### Scenario: Production dependency is proposed

- **WHEN** a change proposes a production embedding model, vector database, queue worker, reranker, or graph store
- **THEN** the change references the production indexing architecture decision record and states whether the relevant decision is approved

#### Scenario: Decision is not approved

- **WHEN** a production infrastructure decision remains open
- **THEN** implementation changes avoid adding that production dependency and remain at provider-neutral contract or local-adapter level

#### Scenario: Retrieval infrastructure is proposed

- **WHEN** a change proposes production embedding, vector database, or reranker implementation
- **THEN** the change references retrieval candidate evaluation evidence, preferably exported JSON or Markdown reports, or explicitly states why candidate evidence is not yet available

#### Scenario: Qdrant is evaluated as primary vector-store candidate

- **WHEN** Qdrant is introduced before production approval
- **THEN** the implementation remains an explicit candidate adapter and does not switch the default retrieval backend

#### Scenario: Qdrant live adapter is added before embedding selection

- **WHEN** live Qdrant ingestion or vector query helpers are added
- **THEN** they accept caller-supplied vectors and do not select a production embedding model

#### Scenario: Embedding adapter interface is added before model selection

- **WHEN** an embedding adapter interface is added before model approval
- **THEN** real hosted or local providers fail closed and the default adapter remains deterministic mock-only

#### Scenario: Qdrant text query orchestration is added before production promotion

- **WHEN** Qdrant text query orchestration is available
- **THEN** it remains opt-in and still requires benchmark evidence before production promotion

#### Scenario: Qdrant source ingestion is added before chunking finalization

- **WHEN** Qdrant source ingestion uses local markdown chunking
- **THEN** the chunking strategy is documented as an evaluation baseline and not a final enterprise parser decision

### Requirement: Production indexing candidates are evaluated consistently

The system SHALL document evaluation criteria for production indexing infrastructure.

#### Scenario: Embedding model is evaluated

- **WHEN** an embedding model is considered
- **THEN** the decision record compares language coverage, retrieval quality, cost, latency, deployment model, data residency, dimensionality, and reranker compatibility

#### Scenario: Vector database is evaluated

- **WHEN** a vector database is considered
- **THEN** the decision record compares filter support, hybrid retrieval, operational complexity, persistence, scaling, backup/restore, ecosystem integration, and local development ergonomics

#### Scenario: Queue worker is evaluated

- **WHEN** a production ingestion worker is considered
- **THEN** the decision record compares lease semantics, retry behavior, cancellation, stale recovery, concurrency, observability, and deployment complexity

### Requirement: Chinese embedding candidates are evaluated before approval

The system SHALL evaluate Chinese-heavy embedding candidates as explicit architecture candidates before approving a production embedding provider.

#### Scenario: Candidate metadata is recorded

- **WHEN** an embedding candidate is defined for evaluation
- **THEN** it records stable id, provider family, model name, deployment mode, language profile, vector dimension, data residency posture, operational complexity, reranker compatibility, and approval status

#### Scenario: Candidate remains unapproved

- **WHEN** an embedding candidate is included in the evaluation catalog
- **THEN** the system treats it as evidence for review and does not enable hosted or local embedding calls by default

#### Scenario: Chinese-heavy workload is evaluated

- **WHEN** the project evaluates an embedding model for the expected workload
- **THEN** the evaluation states whether the candidate is suitable for Chinese-heavy corpora and whether it supports private-network deployment

### Requirement: Embedding decisions use Chinese-heavy seed evidence

The system SHALL require Chinese-heavy benchmark seed evidence before selecting a production embedding provider.

#### Scenario: Embedding candidate is compared

- **WHEN** an embedding candidate is proposed for Chinese-heavy workloads
- **THEN** the proposal references benchmark cases that include enterprise support categories beyond simple exact-match policy lookup

#### Scenario: Seed evidence is not final acceptance

- **WHEN** the local Chinese benchmark seed passes
- **THEN** the result is treated as early comparison evidence and not final production acceptance coverage

### Requirement: GraphRAG storage remains a separate decision

The system SHALL keep graph storage and GraphRAG implementation choices separate from document vector retrieval choices.

#### Scenario: Graph storage is evaluated

- **WHEN** graph storage is considered
- **THEN** the decision record compares ontology/versioning needs, entity/relation lifecycle, traversal query support, full-text/vector hybrid capability, evidence traceability, and operational ownership
