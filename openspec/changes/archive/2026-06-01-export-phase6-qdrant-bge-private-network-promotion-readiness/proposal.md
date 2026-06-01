## Why

The private-network promotion review contract is now documented, but reviewers still have to manually aggregate Qdrant, BGE-M3, Phase 3, and deployment-linkage artifacts. A single export is required for repeatable review.

## What Changes

- Add a local `phase6-qdrant-bge-private-network-promotion-readiness` export.
- Summarize required review inputs, open gates, and decision posture in one machine-readable artifact.
- Wire optional readiness evidence into handoff bundle and refresh.

## Capabilities

### New Capabilities

- `phase6-qdrant-bge-private-network-promotion-readiness`: local readiness export for private-network candidate promotion review.

### Modified Capabilities

- `knowledge-provider`: handoff and refresh can summarize optional private-network promotion readiness evidence.
- `provider-roadmap`: records private-network readiness export as Phase 6 evidence visibility work.

## Impact

- Affected code: new readiness service/export script and handoff integrations.
- Affected tests: focused readiness and handoff assertions.
- Runtime defaults remain unchanged.
