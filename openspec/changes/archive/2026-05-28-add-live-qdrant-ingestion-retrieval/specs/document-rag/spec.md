## ADDED Requirements

### Requirement: Qdrant collection can be prepared explicitly

The system SHALL prepare a configured Qdrant collection only through explicit Qdrant adapter calls.

#### Scenario: Qdrant collection is ready

- **WHEN** the configured Qdrant collection exists or can be created
- **THEN** the Qdrant adapter reports collection readiness as `ready`

#### Scenario: Qdrant collection is unavailable

- **WHEN** the configured Qdrant collection cannot be reached or created
- **THEN** the Qdrant adapter reports readiness as `degraded` with a reason

### Requirement: Qdrant evidence chunks can be upserted

The system SHALL upsert provider-neutral evidence chunks into Qdrant using the established point and payload contract.

#### Scenario: Evidence chunks are upserted

- **WHEN** evidence chunks with vectors are sent to the Qdrant adapter
- **THEN** the adapter writes Qdrant points to the configured collection

#### Scenario: Evidence payload is preserved

- **WHEN** chunks are upserted
- **THEN** source, tenant, document, chunk, citation, text, and ACL metadata remain in the payload

### Requirement: Qdrant vector query maps hits to evidence documents

The system SHALL query Qdrant with an already-created query vector and map valid hits to provider evidence documents.

#### Scenario: Query vector returns hits

- **WHEN** a Qdrant query returns hits with required evidence payload fields
- **THEN** the adapter returns `EvidenceDocument` items with source, document, title, snippet, score, and citation

#### Scenario: Query text embedding remains out of scope

- **WHEN** the Qdrant adapter is called for vector query
- **THEN** the caller supplies the query vector and the adapter does not choose or call an embedding model
