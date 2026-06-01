## ADDED Requirements

### Requirement: Phase 6 BGE-M3 comparison diagnostics exports stay lightweight and evaluation-only

The project SHALL treat Phase 6 BGE-M3 vs mock/fixture diagnostics exports as local evidence visibility work without changing runtime defaults.

#### Scenario: Comparison diagnostics export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes a BGE-M3 comparison diagnostics export
- **THEN** the roadmap records it as Phase 6/Phase 3 bridge evidence visibility rather than runtime promotion

#### Scenario: Comparison diagnostics preserve boundaries

- **WHEN** the export summarizes baseline/candidate quality-latency deltas and deployment linkage
- **THEN** runtime defaults, provider HTTP contracts, and external control-plane ownership remain unchanged
