## ADDED Requirements

### Requirement: Phase 3 cross-case FP/FN smoke remains lightweight evidence maintenance

The project SHALL treat Phase 3 hybrid cross-case FP/FN smoke as lightweight evidence maintenance when it validates risk-signal visibility without changing runtime defaults.

#### Scenario: Cross-case smoke is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes cross-case hybrid FP/FN smoke evidence
- **THEN** the roadmap records it as Phase 3 evidence maintenance and review ergonomics work

#### Scenario: Cross-case smoke preserves boundaries

- **WHEN** cross-case smoke reports false-positive/false-negative risk signals
- **THEN** runtime defaults, provider HTTP contracts, GraphRAG boundaries, and caller ownership remain unchanged
