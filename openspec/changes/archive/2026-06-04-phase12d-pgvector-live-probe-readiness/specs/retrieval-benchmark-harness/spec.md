## ADDED Requirements

### Requirement: Phase 12d pgvector live probe evidence can be exported locally
The retrieval benchmark harness SHALL export a local Phase 12d pgvector live probe readiness report that consolidates pgvector-specific live probe evidence into a shared review artifact.

#### Scenario: pgvector live probe readiness report is exported
- **WHEN** the Phase 12d pgvector live probe readiness export runs
- **THEN** it produces a JSON report and a Markdown report for local review

#### Scenario: pgvector probe posture is explicit
- **WHEN** the readiness report is generated
- **THEN** it records the pgvector probe state, open gates, and review decision using the shared candidate vocabulary

#### Scenario: missing driver or database configuration stays read-only
- **WHEN** pgvector connection posture or the optional PostgreSQL driver is not available locally
- **THEN** the export remains read-only, records the missing prerequisite as an open gate, and does not change runtime defaults

### Requirement: Phase 12d pgvector live probe preserves candidate-only boundaries
The retrieval benchmark harness SHALL keep pgvector probe evaluation as review-only evidence until a separate promotion change is approved.

#### Scenario: pgvector probe evidence is promising but incomplete
- **WHEN** the pgvector live probe surfaces partial local evidence
- **THEN** the result is recorded as `continue_spike` or `keep_current_default`, not as runtime promotion

#### Scenario: pgvector promotion still requires a separate change
- **WHEN** pgvector evidence becomes strong enough for promotion review
- **THEN** the report can record `eligible_for_promotion_review` but runtime defaults remain unchanged until a separate promotion change is approved

#### Scenario: other candidate families remain comparable
- **WHEN** pgvector is evaluated alongside other backend candidates
- **THEN** the report keeps the same decision vocabulary and comparison shape as the rest of the candidate evaluation flow
