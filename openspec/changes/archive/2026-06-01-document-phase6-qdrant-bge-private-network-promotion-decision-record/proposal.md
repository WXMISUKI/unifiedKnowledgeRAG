## Why

After contract, readiness export, and smoke slices are complete, reviewers still need an explicit decision record to avoid ambiguous interpretation of the current promotion state.

## What Changes

- Add a local decision record for the current Qdrant+BGE private-network promotion review cycle.
- Explicitly capture current verdict, open gates, and next-step conditions.
- Keep the slice documentation-only.

## Capabilities

### New Capabilities

- `private-network-promotion-decision-record`: read-only decision record for Qdrant+BGE private-network promotion review.

### Modified Capabilities

- `provider-roadmap`: records this decision record as bridge-governance evidence.
- `knowledge-provider`: records decision artifact as boundary-safe documentation, not runtime promotion.

## Impact

- Affected docs: `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-decision-record.md`.
- Runtime defaults remain unchanged.
