## ADDED Requirements

### Requirement: Phase 3 evidence refresh preserves lightweight promotion boundaries

The project SHALL treat post-fixture evidence regeneration as Phase 3 maintenance when it keeps benchmark artifacts current without changing runtime defaults.

#### Scenario: Evidence refresh is phase-aligned

- **WHEN** benchmark fixture updates require regenerated Chinese-seed evidence
- **THEN** the roadmap records the work as retrieval evidence maintenance rather than runtime retrieval promotion

#### Scenario: Evidence refresh keeps provider boundary unchanged

- **WHEN** Chinese-seed evidence is refreshed
- **THEN** provider contracts, control-plane ownership, and GraphRAG execution boundaries remain unchanged
