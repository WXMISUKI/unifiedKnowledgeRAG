## MODIFIED Requirements

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
