## Why

Phase 2 through Phase 6 now provide a dense evidence chain, but reviewers still lack one explicit acceptance contract that says how this provider handoff should be consumed by a caller or deployment reviewer. Without this contract, `review` statuses are easy to misinterpret as failure or implicit production promotion.

## What Changes

- Add a Phase 7 provider handoff acceptance contract document under `docs/operations/provider-release-readiness/`.
- Define required evidence, optional review evidence, acceptance semantics, and non-goals.
- Preserve existing boundaries: this provider remains evidence/data-plane and does not take over caller control-plane responsibilities.
- Keep this slice documentation-only with no runtime or API behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records a cross-phase handoff acceptance contract as Phase 7 governance evidence.
- `knowledge-provider`: documents caller/deployment reviewer consumption rules over existing handoff evidence.

## Impact

- Affected docs: new Phase 7 acceptance contract doc plus roadmap/progress notes.
- No runtime defaults, retrieval behavior, parser behavior, or graph execution changes.
