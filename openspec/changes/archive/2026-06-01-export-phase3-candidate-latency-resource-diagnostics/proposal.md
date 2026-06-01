## Why

Phase 3 promotion review already has candidate runtime diagnostics, but reviewers still need one compact place to see latency shape and resource posture together. A latency/resource diagnostic view makes it easier to compare the current local seed evidence against deployment readiness without changing runtime defaults.

## What Changes

- Add a local Phase 3 candidate latency/resource diagnostics export under `docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/`.
- Summarize local benchmark latency profile and current resource/deployment posture in a machine-readable report.
- Include the report in provider handoff bundle and handoff refresh as optional review evidence.
- Keep the export read-only and evaluation-only; do not change runtime defaults, API contracts, or promotion decisions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds a Phase 3 latency/resource diagnostics export for candidate promotion review.
- `knowledge-provider`: handoff bundle/refresh can summarize this export as optional Phase 3 evidence.
- `provider-roadmap`: records this as lightweight Phase 3 evidence visibility work.

## Impact

- Affected code: new Phase 3 latency/resource diagnostics service and export script.
- Affected tests: new diagnostics tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown latency/resource diagnostics artifacts.
- Runtime defaults remain unchanged.
