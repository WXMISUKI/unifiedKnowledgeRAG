## ADDED Requirements

### Requirement: Phase 3 evidence summaries in handoff stay lightweight

The project SHALL treat compact Phase 3 retrieval evidence summaries in handoff as lightweight review ergonomics work when they improve discoverability without changing runtime promotion gates.

#### Scenario: Handoff Phase 3 summary is phase-aligned

- **WHEN** an OpenSpec change adds a compact Phase 3 baseline evidence summary row to handoff
- **THEN** the roadmap records it as Phase 3/Phase 6 evidence visibility rather than runtime retrieval promotion

#### Scenario: Handoff Phase 3 summary preserves provider boundary

- **WHEN** handoff includes compact Phase 3 benchmark summary metrics
- **THEN** retrieval defaults, control-plane ownership, and GraphRAG execution boundaries remain unchanged
