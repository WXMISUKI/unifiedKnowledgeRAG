## Why

The current Qdrant+BGE-M3 threshold sweep shows perfect metrics at threshold `0.7`, but the benchmark has only three expected-empty cases. Before treating `0.7` as a serious default candidate, the local Chinese seed needs more business-like unsupported questions that stress false-positive retrieval.

## What Changes

- Expand the Chinese retrieval benchmark with additional expected-empty cases.
- Cover unsupported but plausible enterprise support topics such as membership, invoice, warranty, account, promotion, and finance-adjacent questions.
- Regenerate fixture and Qdrant+BGE evidence so the threshold sweep reflects the larger empty stress set.
- Update documentation to explain that threshold decisions must be based on the expanded empty set.

## Capabilities

### New Capabilities

### Modified Capabilities
- `retrieval-benchmark-harness`: expand local Chinese empty retrieval stress cases and evidence expectations.

## Impact

- Affected fixtures: `tests/fixtures/retrieval_benchmark_cases.json`.
- Affected tests: retrieval benchmark tests.
- Affected docs/evidence: README and Chinese seed benchmark reports.
- No API change, no default threshold change, and no new dependency.
