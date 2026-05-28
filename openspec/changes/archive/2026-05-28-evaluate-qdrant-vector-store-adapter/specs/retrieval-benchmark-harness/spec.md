## ADDED Requirements

### Requirement: Qdrant can be registered as a retrieval candidate

The system SHALL expose Qdrant as an explicit retrieval candidate for benchmark comparison without selecting a production embedding model.

#### Scenario: Qdrant candidate metadata is created

- **WHEN** the Qdrant candidate is requested
- **THEN** candidate metadata identifies Qdrant as the vector store and leaves embedding and reranker choices undecided

#### Scenario: Qdrant candidate remains opt-in

- **WHEN** candidate evaluation is configured
- **THEN** Qdrant is included only when the caller explicitly selects the Qdrant candidate
