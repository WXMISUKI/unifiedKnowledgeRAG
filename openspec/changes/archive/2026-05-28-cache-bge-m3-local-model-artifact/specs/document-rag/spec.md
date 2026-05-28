## ADDED Requirements

### Requirement: Local BGE-M3 model path supports offline retrieval evaluation

The system SHALL support using a pre-downloaded BGE-M3 model directory for local Qdrant retrieval evaluation.

#### Scenario: Offline model path is configured

- **WHEN** `EMBEDDING_MODEL_PATH` points to a downloaded BGE-M3 directory and `EMBEDDING_LOCAL_FILES_ONLY=true`
- **THEN** the local embedding adapter uses the local artifact path without requiring runtime model download
