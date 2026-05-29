## MODIFIED Requirements

### Requirement: Mature RAG pattern research guides production dependency changes

The system SHALL maintain an internal research reference that maps mature Agentic RAG, Retrieval, GraphRAG, hybrid search, and reranking patterns to the provider roadmap before adding new production retrieval dependencies.

#### Scenario: Research note identifies source patterns

- **WHEN** the research note is reviewed
- **THEN** it identifies the mature external pattern families considered and the provider-local reason for considering each one

#### Scenario: Pattern adoption has an evidence gate

- **WHEN** a future change proposes agentic retrieval, query rewriting, hybrid retrieval, reranking, or GraphRAG storage
- **THEN** the change references the research note or fresher benchmark evidence before adding runtime dependencies

#### Scenario: Query rewrite evidence precedes runtime adoption

- **WHEN** a future change proposes enabling query rewriting in runtime retrieval
- **THEN** it references local query rewrite candidate evidence and explicitly reviews expected-empty false-positive risk

#### Scenario: Pattern adoption remains provider-neutral

- **WHEN** a mature pattern is selected for implementation
- **THEN** the implementation preserves the existing provider-neutral HTTP contracts unless a separate approved change modifies those contracts

#### Scenario: Research separates document RAG and GraphRAG priorities

- **WHEN** the roadmap is reviewed
- **THEN** document RAG improvements, hybrid/rerank candidates, and GraphRAG storage are classified separately rather than being implemented as one combined dependency change
