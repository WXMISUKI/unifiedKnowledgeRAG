## Why

The provider now exposes manifest, preflight, capabilities, and invocation examples, but external control planes still need to wire those endpoints together themselves. A small reference integration client gives MyPrivateAgent a concrete, testable binding probe before invoking retrieval or graph capabilities.

## What Changes

- Add a provider integration client that probes manifest, preflight, and capabilities in the recommended order.
- Return a machine-readable binding report with provider identity, bindability, capability statuses, invocation metadata, and example request coverage.
- Keep the client read-only by default; it must not execute RAG retrieval, answer composition, ingestion, index rebuilds, or graph queries.
- Document the integration flow for MyPrivateAgent and other external control planes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: add a local reference integration probe for external control-plane binding.

## Impact

- Adds service-level integration helper code and tests.
- Does not change public provider endpoint behavior.
- Does not introduce new dependencies, model providers, vector databases, graph stores, or network-only assumptions.
