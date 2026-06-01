## ADDED Requirements

### Requirement: Phase 2 parser-expansion decision record is documentation-only governance evidence

The project SHALL allow a Phase 2 parser-expansion decision record that captures the current-cycle verdict and open gates without changing runtime parser defaults.

#### Scenario: Decision record captures keep-baseline verdict

- **WHEN** Phase 2 demand readiness and unsupported-format smoke remain within Markdown baseline expectations
- **THEN** the decision record explicitly records `keep_markdown_baseline` for the current cycle

#### Scenario: Decision record preserves parser boundary

- **WHEN** the decision record is added or updated
- **THEN** non-Markdown parser families remain deferred unless a separate approved promotion change is completed
