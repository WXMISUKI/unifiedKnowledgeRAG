# production-indexing-architecture Delta

## MODIFIED Requirements

### Requirement: Mature RAG pattern research guides production dependency changes

The system SHALL maintain an internal research reference that maps mature Agentic RAG, Retrieval, GraphRAG, hybrid search, and reranking patterns to the provider roadmap before adding new production retrieval dependencies.

#### Scenario: Exact-term evidence precedes hybrid retrieval

- **WHEN** a future change proposes sparse vectors, BM25, dense+sparse hybrid retrieval, or runtime hybrid gating
- **THEN** it references exact-term and identifier benchmark evidence, including dense-only, hybrid recall, hybrid empty-stress, and hybrid gating evidence when available, and explains which retrieval misses or false-positive risks justify the added retrieval complexity
