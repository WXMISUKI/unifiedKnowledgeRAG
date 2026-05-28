## ADDED Requirements

### Requirement: Qdrant vector points preserve retrieval evidence metadata

The system SHALL map indexed evidence chunks to Qdrant point payloads while preserving citation and enterprise metadata fields.

#### Scenario: Evidence chunk becomes Qdrant point

- **WHEN** an evidence chunk is mapped for Qdrant
- **THEN** the point includes a stable id, named vector, source id, document id, chunk id, title, citation, and text payload

#### Scenario: Enterprise metadata is preserved

- **WHEN** an evidence chunk includes tenant, ACL, document version, embedding model, or chunking strategy metadata
- **THEN** the Qdrant payload preserves those fields for later filtering and audit

#### Scenario: Retrieval filter is built

- **WHEN** source ids and tenant id are supplied for Qdrant retrieval
- **THEN** the adapter builds a payload filter that includes tenant and source constraints
