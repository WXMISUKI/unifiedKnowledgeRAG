## Why

The comparison contract is now documented, but reviewers still need to manually compare baseline and candidate artifacts across Phase 3 and Phase 6 evidence outputs. A single machine-readable diagnostics export is needed for repeatable review.

## What Changes

- Add a local `phase6-bge-m3-vs-mock-fixture-diagnostics` export (JSON + Markdown).
- Summarize baseline vs candidate quality/latency deltas and artifact/deployment linkage posture.
- Wire optional diagnostics evidence into provider handoff bundle and handoff refresh.
- Keep the work read-only and evaluation-only.

## Capabilities

### New Capabilities

- `phase6-bge-m3-vs-mock-fixture-diagnostics`: local bridge export for BGE-M3 candidate comparison review.

### Modified Capabilities

- `knowledge-provider`: handoff bundle and refresh can summarize optional BGE-M3 comparison diagnostics.
- `provider-roadmap`: records BGE-M3 comparison diagnostics as Phase 6/Phase 3 bridge evidence visibility.

## Impact

- Affected code: new diagnostics service/export script and handoff integrations.
- Affected tests: focused coverage for diagnostics and optional handoff parsing.
- Runtime defaults and public API contracts remain unchanged.
