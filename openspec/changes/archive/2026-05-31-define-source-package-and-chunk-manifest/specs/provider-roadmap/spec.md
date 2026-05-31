## ADDED Requirements

### Requirement: Source package and chunk manifest advance Phase 2 ingestion evidence
The project SHALL treat source package metadata and chunk manifest diagnostics as Phase 2 document ingestion baseline work when they help operators review source readiness without adding heavy parser or indexing infrastructure.

#### Scenario: Source package work is phase-aligned
- **WHEN** an OpenSpec change adds source package metadata or chunk manifest diagnostics
- **THEN** the roadmap records it as Phase 2 ingestion evidence work

#### Scenario: Source package work preserves lightweight scope
- **WHEN** the provider exposes source package or chunk manifest diagnostics
- **THEN** the provider still does not own source-to-agent binding approval, audit policy, OCR workflows, production parser expansion, embedding selection, vector-store promotion, or GraphRAG execution
