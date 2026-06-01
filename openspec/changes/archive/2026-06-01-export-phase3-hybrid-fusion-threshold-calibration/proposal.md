## Why

Phase 3 already has candidate-level hybrid evidence, FP/FN review, and latency/resource diagnostics, but reviewers still lack one compact calibration view that compares hybrid fusion context and threshold semantics in one place. Current evidence mixes dense threshold sweeps and hybrid RRF retrieval runs, and this can be misread as a runtime-ready threshold promotion signal.

## What Changes

- Add a local Phase 3 hybrid fusion/threshold calibration export under `docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/`.
- Summarize hybrid candidate signals (exact-term, empty-stress, gating, FP/FN, threshold recommendation, deployment/runtime threshold context) in one machine-readable review artifact.
- Include this calibration artifact in provider handoff bundle and handoff refresh as optional review evidence.
- Keep this work read-only and evaluation-only; do not change runtime defaults, API contracts, or promotion decisions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `retrieval-benchmark-harness`: adds a Phase 3 hybrid fusion/threshold calibration export for promotion review context.
- `knowledge-provider`: handoff bundle/refresh can summarize this export as optional Phase 3 evidence.
- `provider-roadmap`: records this as lightweight Phase 3 evidence visibility work.

## Impact

- Affected code: new Phase 3 calibration service and export script.
- Affected tests: new calibration tests plus focused handoff bundle/refresh assertions.
- Affected docs/evidence: local JSON and Markdown calibration artifacts.
- Runtime defaults remain unchanged.
