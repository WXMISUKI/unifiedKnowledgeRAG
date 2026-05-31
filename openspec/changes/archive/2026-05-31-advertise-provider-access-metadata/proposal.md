## Why

The provider supports an optional API key guard for `/api/*`, but external control planes currently need README knowledge to know which paths are public and which headers are accepted. The manifest should expose this access contract in machine-readable form so MyPrivateAgent can bind the component without hard-coding provider-specific auth rules.

## What Changes

- Add machine-readable component access metadata to the provider integration manifest.
- Describe public paths, protected path patterns, accepted API key header schemes, and whether an API key is configured.
- Keep secret values redacted and outside the manifest.
- Update tests and documentation for the manifest access contract.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Provider manifest advertises component access metadata for external control-plane integration.
- `provider-roadmap`: Treat access metadata as Phase 6 integration evidence without moving identity, RBAC, or policy ownership into the provider.

## Impact

- Updates manifest model and builder.
- Updates manifest tests and README/roadmap.
- No new endpoints, dependencies, or runtime default changes.
