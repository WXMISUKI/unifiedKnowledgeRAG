## ADDED Requirements

### Requirement: Phase 12c pgvector candidate backend evidence can be exported locally
The retrieval benchmark harness SHALL export a local Phase 12c pgvector candidate backend readiness report that consolidates pgvector-specific evidence into a shared review artifact.

#### Scenario: pgvector readiness report is exported
- **WHEN** the Phase 12c pgvector candidate backend readiness export runs
- **THEN** it produces a JSON report and a Markdown report for local review

#### Scenario: pgvector candidate posture is explicit
- **WHEN** the readiness report is generated
- **THEN** it records the pgvector candidate state, open gates, and review decision using the shared candidate vocabulary

#### Scenario: missing backend configuration stays read-only
- **WHEN** pgvector connection posture is not configured locally
- **THEN** the export remains read-only, records the missing configuration as an open gate, and does not change runtime defaults

### Requirement: Phase 12c pgvector candidate review preserves candidate-only boundaries
The retrieval benchmark harness SHALL keep pgvector candidate evaluation as review-only evidence until a separate promotion change is approved.

#### Scenario: pgvector evidence is promising but incomplete
- **WHEN** the pgvector spike surfaces partial local evidence
- **THEN** the result is recorded as `continue_spike` or `keep_current_default`, not as runtime promotion

#### Scenario: pgvector promotion still requires a separate change
- **WHEN** pgvector evidence becomes strong enough for promotion review
- **THEN** the report can record `eligible_for_promotion_review` but runtime defaults remain unchanged until a separate promotion change is approved

#### Scenario: other candidate families remain comparable
- **WHEN** pgvector is evaluated alongside other backend candidates
- **THEN** the report keeps the same decision vocabulary and comparison shape as the rest of the candidate evaluation flow
