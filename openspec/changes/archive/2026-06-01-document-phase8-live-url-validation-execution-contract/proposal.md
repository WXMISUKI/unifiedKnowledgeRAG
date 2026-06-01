## Why

Phase 7 has already clarified that local handoff is ready while runtime promotion remains gated, but a concrete live-URL execution contract is still missing. Without this contract, deployed smoke execution can drift into ad hoc endpoint usage or be over-interpreted as runtime-promotion approval.

## What Changes

- Add a Phase 8 live-URL validation execution contract under `docs/operations/live-url-validation/`.
- Define execution inputs, allowed endpoint scope, status semantics, and non-goals.
- Keep this slice documentation-only and boundary-safe.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records Phase 8 live deployment validation execution boundary.
- `knowledge-provider`: documents how live URL validation should be consumed as read-only operational evidence.

## Impact

- Affected docs: one new Phase 8 execution contract plus roadmap/tracker notes.
- No runtime behavior changes, no API changes, no retrieval or parser behavior changes.
