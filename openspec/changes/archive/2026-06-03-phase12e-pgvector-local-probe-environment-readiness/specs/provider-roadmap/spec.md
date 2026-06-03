## ADDED Requirements

### Requirement: Phase 12e pgvector local probe environment remains provider-first and evaluation-only
The project SHALL treat the Phase 12e pgvector local probe environment as lightweight review work that packages optional local setup evidence without changing runtime defaults or ownership boundaries.

#### Scenario: Phase 12e readiness export is published
- **WHEN** the pgvector local probe environment readiness report is exported
- **THEN** it records the environment package state, open gates, and keep-default boundary

#### Scenario: pgvector environment work stays reversible
- **WHEN** the pgvector environment package exposes useful local evidence
- **THEN** the provider still keeps pgvector out of runtime defaults until a separate promotion change is approved

#### Scenario: provider boundaries remain unchanged
- **WHEN** the pgvector environment package is reviewed
- **THEN** caller control-plane ownership, GraphRAG execution, parser expansion, and answer policy remain outside this change
