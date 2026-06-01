## Why

Phase 3 already has multi-chunk aggregation candidate evidence and relation-aware grading evidence, but reviewers still need a compact smoke that shows the over-broad negative control stays visible. Without that, it is easy to overread a positive aggregation result and miss the unsupported relationship case that should block runtime promotion.

## What Changes

- Add a local Phase 3 aggregation/relation negative-control smoke summary report.
- Validate the positive split-chunk control, the same-document negative control, and the relation-aware grading label for the unsupported relation case.
- Export JSON and Markdown smoke artifacts under `docs/smoke/`.
- Surface the smoke as optional review evidence in provider handoff bundle and handoff refresh.
- Keep the smoke read-only and evaluation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds exportable Phase 3 aggregation/relation negative-control smoke evidence.
- `knowledge-provider`: handoff bundle/refresh can summarize this smoke as optional Phase 3 evidence.
- `provider-roadmap`: records this as lightweight Phase 3 evidence maintenance work.

## Impact

- Affected code: new smoke service and export script.
- Affected tests: new smoke tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: new smoke artifacts and tracker/roadmap references.
- Runtime defaults and promotion decisions remain unchanged.
