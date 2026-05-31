## Why

Deployment readiness now has an operator guide, but operators still need a compact reference for the actual config surface: env vars, mount points, and which values are safe defaults versus deployment inputs.

## What Changes

- Add a deployment configuration reference under `docs/operations/deployment-readiness/`.
- Document the runtime environment variables, recommended deployment modes, mounted paths, and refresh commands.
- Keep it documentation-only and aligned with current exported evidence.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records deployment configuration reference as Phase 6 operations documentation.

## Impact

- Affected docs: `docs/operations/deployment-readiness/config-reference.md`
- Affected tracker: `docs/progress/provider-improvement-tracker.md`
- No runtime code changes, no API changes, no strategy changes
