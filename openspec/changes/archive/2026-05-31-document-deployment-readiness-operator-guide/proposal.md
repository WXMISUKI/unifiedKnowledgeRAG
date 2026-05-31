## Why

Deployment readiness is already exported as evidence, but the project still needs a concise operator-facing guide that turns review-state output into concrete deployment actions.

## What Changes

- Add an operator guide for `docs/operations/deployment-readiness`.
- Explain how to read the current `review` status and which items remain deployment preconditions.
- Document the standard maintenance commands for refresh, readiness export, reindex planning, and deployed smoke.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: treats deployment readiness guide as Phase 6 operations documentation, not runtime promotion.

## Impact

- Affected docs: `docs/operations/deployment-readiness/operator-guide.md`
- Affected tracker: `docs/progress/provider-improvement-tracker.md`
- No runtime code changes, no API changes, no strategy changes
