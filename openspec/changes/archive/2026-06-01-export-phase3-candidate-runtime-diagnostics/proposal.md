## Why

Phase 3 promotion readiness already summarizes open gates, but reviewers still need one more local artifact that focuses on candidate runtime prerequisites: embedding provider state, model artifact state, retrieval backend state, and deployment-adjacent evidence presence. Without this diagnostic view, runtime promotion review remains scattered across deployment readiness, retrieval readiness, and handoff rows.

## What Changes

- Add a local Phase 3 candidate runtime diagnostics export under `docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/`.
- Summarize candidate runtime prerequisite checks and open prerequisites in a machine-readable report.
- Include this report in provider handoff bundle and handoff refresh as optional review evidence.
- Keep the export read-only and evaluation-only; do not change runtime defaults, API contracts, or promotion decisions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds a Phase 3 runtime diagnostics export for candidate promotion review.
- `knowledge-provider`: handoff bundle/refresh can summarize this export as optional Phase 3 evidence.
- `provider-roadmap`: records this as lightweight Phase 3 evidence visibility work.

## Impact

- Affected code: new Phase 3 diagnostics service and export script.
- Affected tests: new diagnostics tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown runtime diagnostics artifacts.
- Runtime defaults remain unchanged.
