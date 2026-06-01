## Why

Phase 6 already has deployment readiness and a deployed provider smoke, but we still lack a contract that says what "deployed field validation" means once a real URL exists. Without that contract, the review path is easy to misread as an automatic promotion gate instead of a live evidence check.

## What Changes

- Add a local Phase 6 contract document for deployed field validation.
- Define the required live-URL evidence, handoff expectations, and boundary-safe non-goals.
- Keep this slice documentation-only; no runtime default changes, no live traffic orchestration, and no deployment automation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records deployed field validation as Phase 6 operations evidence.
- `knowledge-provider`: records provider-owned live URL evidence boundary as read-only, operator-facing review context.

## Impact

- Affected docs: one new contract markdown plus tracker refresh.
- No code-path, deployment, or API behavior impact.
