## ADDED Requirements

### Requirement: Phase 6 BGE-M3 comparison smoke stays lightweight and read-only

The project SHALL treat Phase 6 BGE-M3 comparison smoke summaries as local evidence maintenance without changing runtime defaults.

#### Scenario: Comparison smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes BGE-M3 comparison smoke evidence
- **THEN** the roadmap records it as Phase 6 evidence maintenance and not runtime promotion

#### Scenario: Comparison smoke preserves boundaries

- **WHEN** the smoke checks comparison evidence-chain prerequisites
- **THEN** it does not execute retrieval changes, model download, embedding execution, or control-plane policy
