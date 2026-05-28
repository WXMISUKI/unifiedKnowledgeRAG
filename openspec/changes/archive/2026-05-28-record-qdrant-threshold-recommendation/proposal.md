## Why

The expanded Chinese seed benchmark now shows that `RAG_SCORE_THRESHOLD=0.7` is the strongest local Qdrant+BGE-M3 threshold candidate, while lower thresholds return unsupported evidence for expected-empty questions. We need to record that recommendation as evidence without silently changing production defaults.

## What Changes

- Add a local threshold recommendation helper that reads a Qdrant+BGE threshold sweep report and selects the lowest threshold that satisfies explicit quality gates.
- Export the recommendation as JSON and Markdown evidence.
- Add CLI support for generating the recommendation from an existing sweep report.
- Document `0.7` as the current local seed recommendation, not a production default.

## Capabilities

### New Capabilities

### Modified Capabilities
- `retrieval-benchmark-harness`: add local Qdrant threshold recommendation evidence derived from threshold sweep results.

## Impact

- Affected code: `app.services.retrieval_benchmark`, `scripts/export_qdrant_bge_smoke_evidence.py`.
- Affected docs/evidence: `README.md`, `docs/benchmark/chinese-seed/retrieval-candidates`.
- Affected tests: retrieval benchmark tests.
- No runtime default change, no public API change, and no new dependency.
