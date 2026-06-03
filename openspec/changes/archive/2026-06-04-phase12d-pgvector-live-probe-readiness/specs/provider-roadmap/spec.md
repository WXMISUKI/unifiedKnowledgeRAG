## ADDED Requirements

### Requirement: Phase 12d pgvector live probe remains provider-first and evaluation-only
The project SHALL treat the Phase 12d pgvector live probe as lightweight review work that validates a local pgvector deployment without changing runtime defaults or ownership boundaries.

#### Scenario: Phase 12d readiness export is published
- **WHEN** the pgvector live probe readiness report is exported
- **THEN** it records the probe state, open gates, and keep-default boundary

#### Scenario: pgvector probe work stays reversible
- **WHEN** the pgvector probe surfaces useful local evidence
- **THEN** the provider still keeps pgvector out of runtime defaults until a separate promotion change is approved

#### Scenario: provider boundaries remain unchanged
- **WHEN** the pgvector probe is reviewed
- **THEN** caller control-plane ownership, GraphRAG execution, parser expansion, and answer policy remain outside this change
