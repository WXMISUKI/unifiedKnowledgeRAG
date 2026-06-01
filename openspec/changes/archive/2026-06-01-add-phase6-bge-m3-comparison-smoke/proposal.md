## Why

The BGE-M3 comparison diagnostics export is available, but reviewers still lack a compact smoke check for evidence-chain completeness across contract, diagnostics, and prerequisite artifacts.

## What Changes

- Add a local `phase6-bge-m3-comparison-smoke` read-only smoke report.
- Validate presence and parseability of key comparison artifacts.
- Wire optional smoke evidence into provider handoff bundle and handoff refresh.

## Capabilities

### New Capabilities

- `phase6-bge-m3-comparison-smoke`: read-only smoke summary for BGE-M3 comparison evidence-chain readiness.

### Modified Capabilities

- `knowledge-provider`: handoff and refresh can summarize optional BGE-M3 comparison smoke evidence.
- `provider-roadmap`: records BGE-M3 comparison smoke as Phase 6 evidence maintenance work.

## Impact

- Affected code: new smoke service/export script plus handoff wiring.
- Affected tests: focused smoke and handoff assertions.
- Runtime defaults and API contracts remain unchanged.
