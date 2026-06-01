## Why

Phase 3 and Phase 6 bridge evidence now exists in separate readiness, diagnostics, and smoke exports, but hybrid runtime promotion still lacks a single machine-readable review artifact that consolidates final decision prerequisites. Without this export, reviewers must manually stitch multiple files and can miss open gates.

## What Changes

- Add a local Phase 3 hybrid runtime promotion decision readiness export under `docs/benchmark/chinese-seed/hybrid-runtime-promotion/`.
- Summarize required Phase 3 and Phase 6 bridge signals, open gates, and current decision posture in one report.
- Surface this artifact in provider handoff bundle and provider handoff refresh as optional review evidence.
- Keep this work read-only and evaluation-only; do not change runtime defaults.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds exportable final hybrid runtime promotion decision readiness evidence.
- `knowledge-provider`: handoff bundle/refresh can summarize this export as optional Phase 3 evidence.
- `provider-roadmap`: records this slice as lightweight Phase 3 evidence visibility work.

## Impact

- Affected code: new readiness service and export script.
- Affected tests: new readiness tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown readiness artifacts.
- Runtime defaults remain unchanged.
