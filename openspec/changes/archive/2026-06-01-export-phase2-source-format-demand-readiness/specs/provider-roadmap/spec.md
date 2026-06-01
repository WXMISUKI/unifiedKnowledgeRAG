## ADDED Requirements

### Requirement: Phase 2 source-format demand readiness export stays lightweight and evidence-only

The project SHALL treat Phase 2 source-format demand readiness export as local evidence visibility work when it summarizes parser-expansion demand signals without changing runtime defaults.

#### Scenario: Readiness export is phase-aligned

- **WHEN** an OpenSpec change adds or refreshes Phase 2 source-format demand readiness export
- **THEN** roadmap tracking records it as Phase 2 ingestion evidence visibility work, not parser runtime promotion

#### Scenario: Readiness export preserves baseline boundary

- **WHEN** the report summarizes unsupported/non-markdown demand signals and open gates
- **THEN** Markdown remains the runtime parser baseline and non-Markdown parser families remain deferred
