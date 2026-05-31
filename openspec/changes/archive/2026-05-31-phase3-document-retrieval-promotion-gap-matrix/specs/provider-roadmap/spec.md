## ADDED Requirements

### Requirement: Phase 3 retrieval promotion gap matrix is lightweight review ergonomics

The project SHALL treat a local Phase 3 retrieval promotion gap matrix as lightweight evidence review work when it consolidates current candidate evidence and open promotion gaps without changing runtime defaults.

#### Scenario: Gap matrix is published

- **WHEN** an OpenSpec change adds or refreshes the Phase 3 retrieval promotion gap matrix
- **THEN** the roadmap records it as Phase 3 evidence review work rather than runtime promotion

#### Scenario: Gap matrix is read-only

- **WHEN** the gap matrix is reviewed
- **THEN** it does not change retrieval defaults, provider HTTP contracts, or promotion gates
