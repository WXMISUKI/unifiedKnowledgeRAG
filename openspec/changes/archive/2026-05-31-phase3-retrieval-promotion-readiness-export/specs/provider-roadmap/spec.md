## ADDED Requirements

### Requirement: Phase 3 readiness export is lightweight review visibility

The project SHALL treat a local Phase 3 retrieval promotion readiness export as lightweight Phase 3 evidence visibility work when it consolidates current promotion gaps without changing runtime defaults.

#### Scenario: Readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes the Phase 3 readiness export
- **THEN** the roadmap records it as Phase 3 evidence visibility rather than runtime promotion

#### Scenario: Readiness export preserves provider boundary

- **WHEN** the readiness export is reviewed
- **THEN** it does not change retrieval defaults, provider HTTP contracts, or promotion gates
