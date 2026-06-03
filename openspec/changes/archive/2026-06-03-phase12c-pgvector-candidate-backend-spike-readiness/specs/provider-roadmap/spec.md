## ADDED Requirements

### Requirement: Phase 12c pgvector candidate backend spike remains provider-first and evaluation-only
The project SHALL treat the Phase 12c pgvector candidate backend spike as lightweight review work that consolidates pgvector-specific evidence without changing runtime defaults or ownership boundaries.

#### Scenario: Phase 12c readiness export is published
- **WHEN** the pgvector candidate readiness report is exported
- **THEN** it records the pgvector candidate review state, open gates, and keep-default boundary

#### Scenario: pgvector candidate work stays reversible
- **WHEN** the pgvector spike exposes useful local evidence
- **THEN** the provider still keeps pgvector out of runtime defaults until a separate promotion change is approved

#### Scenario: provider boundaries remain unchanged
- **WHEN** the pgvector spike is reviewed
- **THEN** caller control-plane ownership, GraphRAG execution, parser expansion, and answer policy remain outside this change
