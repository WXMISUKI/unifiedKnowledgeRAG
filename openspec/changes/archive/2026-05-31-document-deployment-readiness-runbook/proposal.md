## Why

Deployment readiness now has an operator guide and a configuration reference, but the phase still lacks a single sequential runbook that tells operators what to do first, next, and last.

## What Changes

- Add a deployment readiness runbook under `docs/operations/deployment-readiness/`.
- Sequence the current docs and export commands into a concise operator workflow.
- Keep the runbook documentation-only.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records deployment readiness runbook as Phase 6 operations documentation.

## Impact

- Affected docs: `docs/operations/deployment-readiness/runbook.md`
- Affected tracker: `docs/progress/provider-improvement-tracker.md`
- No runtime code changes, no API changes, no strategy changes
