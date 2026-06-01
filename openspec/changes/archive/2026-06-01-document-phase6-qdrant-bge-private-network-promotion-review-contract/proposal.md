## Why

The project now has separate Phase 6 readiness artifacts for Qdrant and BGE-M3, but private-network promotion review still lacks a single contract that defines required inputs, review states, and non-goals.

## What Changes

- Add a local read-only contract for `Qdrant + BGE-M3` private-network promotion review.
- Define required evidence classes and private-network review states.
- Keep this slice documentation-only and boundary-safe.

## Capabilities

### New Capabilities

- `private-network-promotion-review-contract`: review contract for Qdrant+BGE-M3 private-network promotion evidence.

### Modified Capabilities

- `provider-roadmap`: records this contract as Phase 6/Phase 3 bridge governance evidence.
- `knowledge-provider`: records the provider-owned read-only boundary for private-network promotion review.

## Impact

- Affected docs: `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-review-contract.md`.
- Affected specs: `provider-roadmap`, `knowledge-provider`.
- Runtime defaults and HTTP contracts remain unchanged.
