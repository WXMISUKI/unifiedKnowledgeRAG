## ADDED Requirements

### Requirement: Ready parser artifacts can feed local ingestion orchestration
The normalized parser artifact boundary SHALL expose enough materialized source metadata for a separate local ingestion loop to reuse existing markdown-based onboarding and ingestion flows.

#### Scenario: Ready artifact exposes ingestion loop inputs
- **WHEN** a normalized parser artifact boundary report has `decision=go`
- **THEN** it includes materialized markdown path, source overlay path, source id, title, artifact id, parser id, and content digest
- **AND** those fields can be passed to the parser artifact local ingestion loop without changing existing retrieval or answer contracts

#### Scenario: Non-go artifact does not feed ingestion
- **WHEN** a normalized parser artifact boundary report has `decision=review` or `decision=blocked`
- **THEN** downstream ingestion orchestration must not claim local ingestion readiness from that artifact
- **AND** it records the artifact boundary reason instead of running ingestion
