## Why

Private-network promotion readiness export is available, but there is no compact smoke artifact that validates evidence-chain completeness and parseability in one place.

## What Changes

- Add a local read-only smoke summary for Qdrant+BGE private-network promotion evidence.
- Validate contract/readiness/smoke prerequisites without changing runtime behavior.
- Wire optional smoke evidence into handoff bundle and handoff refresh.

## Capabilities

### New Capabilities

- `phase6-qdrant-bge-private-network-promotion-smoke`: read-only smoke evidence for private-network promotion review.

### Modified Capabilities

- `knowledge-provider`: handoff and refresh can summarize optional private-network promotion smoke evidence.
- `provider-roadmap`: records private-network promotion smoke as Phase 6 evidence maintenance.

## Impact

- Affected code: new smoke service/export script and handoff integrations.
- Affected tests: focused smoke and handoff assertions.
- Runtime defaults remain unchanged.
