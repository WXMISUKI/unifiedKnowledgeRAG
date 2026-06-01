## ADDED Requirements

### Requirement: Phase 6 private-network promotion smoke stays lightweight and read-only

The project SHALL treat private-network promotion smoke summaries as local Phase 6 evidence maintenance without changing runtime defaults.

#### Scenario: Private-network promotion smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes private-network promotion smoke evidence
- **THEN** the roadmap records it as Phase 6 evidence maintenance and not runtime promotion

#### Scenario: Private-network promotion smoke preserves boundaries

- **WHEN** smoke checks run
- **THEN** they do not execute runtime retrieval changes, model downloads, deployment automation, or control-plane policies
