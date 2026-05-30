## ADDED Requirements

### Requirement: Source fingerprint diagnostics advance Phase 2 ingestion evidence
The project SHALL treat source document fingerprint and drift diagnostics as Phase 2 document ingestion baseline evidence when they help operators verify local source freshness without changing retrieval behavior.

#### Scenario: Fingerprint diagnostics are phase-aligned
- **WHEN** an OpenSpec change adds read-only source document fingerprint diagnostics
- **THEN** the change identifies Phase 2 as the roadmap phase it advances

#### Scenario: Fingerprint diagnostics do not imply ingestion promotion
- **WHEN** the provider reports source document drift
- **THEN** it does not automatically create ingestion jobs, rebuild indexes, promote chunking strategies, or change retrieval defaults
