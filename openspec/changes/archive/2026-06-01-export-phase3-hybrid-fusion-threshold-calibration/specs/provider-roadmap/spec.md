## ADDED Requirements

### Requirement: Phase 3 hybrid fusion calibration exports stay lightweight and evaluation-only

The project SHALL treat Phase 3 hybrid fusion/threshold calibration exports as lightweight evidence visibility work when they summarize candidate calibration context without changing runtime defaults.

#### Scenario: Calibration export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a Phase 3 hybrid fusion/threshold calibration export
- **THEN** the roadmap records it as Phase 3 evidence visibility work rather than runtime promotion

#### Scenario: Calibration export preserves boundaries

- **WHEN** calibration evidence summarizes candidate hybrid fusion and threshold context
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged
