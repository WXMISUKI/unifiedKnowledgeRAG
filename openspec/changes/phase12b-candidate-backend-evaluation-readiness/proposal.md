## Why

Phase 12 (candidate backend evaluation strategy) already defines short-term
MyPrivateAgent local consumption priority, and mid-term open-source engine spike
方向. The next concrete local milestone is a single evidence slice that
answers:

- Which candidate backend families are currently review-ready.
- Which local evidence gates are still open before any backend promotion.
- What explicit constraints keep runtime defaults unchanged.

At present, candidate-specific evidence already exists in many Phase 3/6 artifacts
(Qdrant vector-store, BGE-M3 quality/latency, hybrid FP/FN/aggregation checks,
deployment/deployed readiness), but it is spread across independent reports.
Without a dedicated Phase 12b readiness consolidation, each contributor must
manually cross-join artifacts.

This change adds a lightweight, read-only Phase 12b readiness contract and
artifact export so that candidate backend evaluation review has one shared entry
point.

## What Changes

- Add a candidate backend evaluation readiness contract that is scoped to
  backend candidates only and keeps the provider read-only.
- Add a local readiness exporter that consolidates required/optional candidate
  candidate evidence into one Phase 12b artifact.
- Add a compact readiness smoke that validates artifact continuity before
  candidate backend planning discussions.
- Expose the new artifact in handoff bundle and refresh flows as optional evidence.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `retrieval-benchmark-harness`: keep candidate backend evidence review as
  read-only candidate evaluation until explicit promotion slice.
- `provider-roadmap`: add a Phase 12b local candidate-backend evaluation
  readiness checkpoint.

## Impact

- Adds `docs/operations/candidate-backend-evaluation-readiness/` evidence files.
- Adds `app/services/phase12b_candidate_backend_evaluation_readiness.py` for
  consolidated readiness aggregation.
- Adds optional smoke file and export script under `docs/smoke/candidate-backend-evaluation`.
- Adds handoff bundle + refresh inclusion as optional review evidence.
- No runtime/default behavior changes.
