## ADDED Requirements

### Requirement: Second-source review evidence is classified before implementation changes
The project SHALL classify second-source aggregate review evidence before proposing retrieval, chunking, or provenance implementation changes.

#### Scenario: Review classification precedes strategy work
- **WHEN** aggregate real-business evidence is `review` for a second real source
- **THEN** the next provider-side slice first classifies whether the issue is negative-control leakage, markdown provenance mismatch, query mismatch, or another concrete failure class
- **AND** it does not immediately promote query rewrite, rerank, hybrid retrieval, or GraphRAG work
