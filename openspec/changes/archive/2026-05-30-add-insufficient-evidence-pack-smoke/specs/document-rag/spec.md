## ADDED Requirements

### Requirement: RAG insufficient-evidence packs are executable smoke evidence
The document RAG evidence pack contract SHALL be covered by executable smoke evidence for both answerable and insufficient-evidence paths.

#### Scenario: Empty retrieval pack is covered by smoke
- **WHEN** provider contract smoke validates document RAG retrieval
- **THEN** smoke evidence includes an insufficient-evidence retrieval pack with zero evidence count and no allowed citations

#### Scenario: Empty answer pack is covered by smoke
- **WHEN** provider contract smoke validates document RAG answer behavior
- **THEN** smoke evidence includes an insufficient-evidence answer pack with `answer_status=insufficient_evidence` and no endorsed answer citations
