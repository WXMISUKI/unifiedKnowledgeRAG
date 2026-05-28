## MODIFIED Requirements

### Requirement: Production indexing choices are decision-gated
The system SHALL require an explicit architecture decision record and retrieval benchmark evidence before adding production embedding, vector store, queue worker, reranker, graph storage, or production chunking dependencies.

#### Scenario: Production dependency is proposed

- **WHEN** a change proposes a production embedding model, vector database, queue worker, reranker, graph store, or production chunking implementation
- **THEN** the change references the production indexing architecture decision record and states whether the relevant decision is approved

#### Scenario: Decision is not approved

- **WHEN** a production infrastructure decision remains open
- **THEN** implementation changes avoid adding that production dependency and remain at provider-neutral contract, local-adapter, or local-evaluation level

#### Scenario: Retrieval infrastructure is proposed

- **WHEN** a change proposes production embedding, vector database, reranker, hybrid retrieval, or chunking implementation
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

#### Scenario: Chunking strategy remains evaluation-only

- **WHEN** a chunking strategy candidate is documented before production approval
- **THEN** runtime ingestion defaults remain unchanged until runnable benchmark evidence and an explicit decision approve the strategy
