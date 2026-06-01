## ADDED Requirements

### Requirement: Phase 3 candidate runtime diagnostics can be exported locally

The system SHALL export a local Phase 3 candidate runtime diagnostics report that summarizes runtime-adjacent promotion prerequisites.

#### Scenario: Runtime diagnostics export writes artifacts

- **WHEN** the Phase 3 candidate runtime diagnostics export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/`

#### Scenario: Runtime diagnostics summarizes prerequisite checks

- **WHEN** the export completes
- **THEN** the report includes retrieval backend state, embedding provider state, model artifact readiness, Phase 3 readiness evidence status, and deployed smoke evidence presence

#### Scenario: Runtime diagnostics export remains read-only

- **WHEN** the runtime diagnostics report is exported
- **THEN** runtime defaults, public HTTP APIs, and promotion decisions remain unchanged
