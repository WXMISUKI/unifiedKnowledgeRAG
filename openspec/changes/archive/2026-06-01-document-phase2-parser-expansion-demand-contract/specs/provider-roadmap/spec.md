## ADDED Requirements

### Requirement: Phase 2 parser expansion demand SHALL be explicitly contract-reviewed

The project SHALL maintain a documentation-only parser expansion demand contract before non-Markdown parser expansion is proposed.

#### Scenario: Parser demand contract captures Markdown baseline

- **WHEN** a reviewer evaluates parser expansion prerequisites
- **THEN** the contract states Markdown as the baseline and records non-Markdown parser work as deferred until evidence requires it

#### Scenario: Parser demand contract preserves lightweight boundary

- **WHEN** the contract is published
- **THEN** runtime defaults, parser dependencies, and control-plane ownership remain unchanged
