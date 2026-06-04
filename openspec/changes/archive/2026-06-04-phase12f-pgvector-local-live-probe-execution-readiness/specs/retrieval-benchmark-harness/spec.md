## ADDED Requirements

### Requirement: Phase 12f pgvector local live-probe execution readiness can be exported locally
The retrieval benchmark harness SHALL export a local Phase 12f pgvector local live-probe execution readiness report that consolidates Phase 12e environment readiness, the current Phase 12d live-probe status, and rerun guidance into a shared review artifact.

#### Scenario: Local execution readiness report is exported
- **WHEN** the Phase 12f pgvector local live-probe execution readiness export runs
- **THEN** it produces a JSON report and a Markdown report for local review

#### Scenario: Execution path is explicit
- **WHEN** the readiness report is generated
- **THEN** it records the execution mode, the rerun target, and the live-probe status before rerun

#### Scenario: Missing local prerequisites stay read-only
- **WHEN** the Phase 12e environment readiness or the rerun documentation is not available locally
- **THEN** the export remains read-only, records the missing prerequisite as an open gate, and does not change runtime defaults

### Requirement: Phase 12f pgvector local live-probe execution readiness preserves candidate-only boundaries
The retrieval benchmark harness SHALL keep pgvector local live-probe execution as review-only evidence until a separate promotion change is approved.

#### Scenario: Execution evidence is promising but incomplete
- **WHEN** the local live-probe rerun path is ready but the live probe has not yet been refreshed
- **THEN** the result is recorded as `continue_spike` or `review`, not as runtime promotion

#### Scenario: Pgvector promotion still requires a separate change
- **WHEN** the local live-probe rerun produces stronger evidence
- **THEN** the report can record `eligible_for_promotion_review` but runtime defaults remain unchanged until a separate promotion change is approved

#### Scenario: Other candidate families remain comparable
- **WHEN** pgvector local live-probe execution is evaluated alongside other backend candidates
- **THEN** the report keeps the same decision vocabulary and comparison shape as the rest of the candidate evaluation flow
