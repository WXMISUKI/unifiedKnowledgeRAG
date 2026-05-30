## Why

The provider integration probe is now available as code, but external control-plane onboarding still needs durable evidence that can be reviewed, archived, and attached to MyPrivateAgent registration decisions. Exporting the probe as JSON and Markdown closes that gap without expanding runtime scope.

## What Changes

- Add export helpers for provider integration probe reports.
- Add a local script that writes machine-readable JSON and human-readable Markdown evidence.
- Include provider identity, contract version, requested requirements, capability binding status, invocation paths, example request coverage, preflight checks, and errors.
- Document the export command and generated evidence location.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: provider integration probe evidence can be exported for external control-plane onboarding.

## Impact

- Adds local service helpers, script, tests, and docs.
- Writes files under `docs/integration/provider-binding/`.
- Does not change provider HTTP APIs, execute RAG/answer/graph capabilities, or introduce new dependencies.
