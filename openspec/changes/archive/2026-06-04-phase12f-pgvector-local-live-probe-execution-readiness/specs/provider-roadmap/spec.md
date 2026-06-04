## ADDED Requirements

### Requirement: Phase 12f pgvector local live-probe execution readiness remains optional and execution-oriented
The project SHALL treat the Phase 12f pgvector local live-probe execution readiness slice as lightweight review work that packages the rerun path for the pgvector live probe without changing runtime defaults or ownership boundaries.

#### Scenario: Phase 12f readiness export is published
- **WHEN** the pgvector local live-probe execution readiness report is exported
- **THEN** it records the Phase 12e environment readiness status, the current Phase 12d live-probe status, and the rerun boundary

#### Scenario: Phase 12f remains developer-owned
- **WHEN** the pgvector local live-probe execution rerun is reviewed
- **THEN** it remains optional and local-only, and it does not move PostgreSQL governance, migration policy, or runtime defaults into the provider

#### Scenario: Provider boundaries remain unchanged
- **WHEN** the pgvector local live-probe execution path is reviewed
- **THEN** caller control-plane ownership, GraphRAG execution, parser expansion, and answer policy remain outside this change
