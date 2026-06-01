## Why

Phase 3 already has benchmark and FP/FN review artifacts, but we still lack a compact smoke report that specifically checks whether cross-case hybrid risk signals stay visible across key risk families (empty false-positive traps, identifier-heavy positives, and policy-nuance positives). This makes regression review slower and less explicit.

## What Changes

- Add a local Phase 3 hybrid cross-case FP/FN smoke summary report.
- Validate presence and alignment of key cross-case risk signals using existing baseline and FP/FN review evidence.
- Export JSON and Markdown smoke artifacts under `docs/smoke/`.
- Surface this smoke as optional review evidence in provider handoff bundle and handoff refresh.
- Keep the smoke read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds exportable Phase 3 hybrid cross-case FP/FN smoke evidence.
- `knowledge-provider`: handoff bundle/refresh can summarize this smoke as optional Phase 3 evidence.
- `provider-roadmap`: records this as lightweight Phase 3 evidence maintenance work.

## Impact

- Affected code: new smoke service and export script.
- Affected tests: new smoke tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: new smoke artifacts and tracker/roadmap references.
- Runtime defaults and promotion decisions remain unchanged.
