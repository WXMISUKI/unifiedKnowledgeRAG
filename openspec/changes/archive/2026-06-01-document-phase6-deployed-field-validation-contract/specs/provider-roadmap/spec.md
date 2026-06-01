## ADDED Requirements

### Requirement: Phase 6 deployed field validation SHALL be explicitly contract-reviewed

The project SHALL maintain a documentation-only contract for deployed field validation before any runtime default promotion is considered.

#### Scenario: Deployed field validation contract is phase-aligned

- **WHEN** a reviewer evaluates a real deployed URL and its smoke evidence
- **THEN** the contract identifies Phase 6 as the roadmap phase and keeps the scope read-only

#### Scenario: Deployed field validation contract preserves provider boundaries

- **WHEN** the contract is published or refreshed
- **THEN** runtime defaults, provider HTTP contracts, and control-plane ownership remain unchanged
