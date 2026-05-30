## Why

After adding a provider manifest, MyPrivateAgent can discover this external knowledge module, but it still needs to combine manifest, health, capabilities, and schema-reference checks on its own before binding. A provider-owned preflight endpoint gives the control plane a single read-only compatibility summary that is easier to automate and less likely to drift.

## What Changes

- Add `GET /api/provider/preflight` as a read-only preflight endpoint.
- Report provider identity, contract version, health status, required capability coverage, schema-reference coverage, and bindability.
- Extract shared health/capability builders so routers, preflight, and tests use the same source of truth.
- Extend provider contract smoke and README documentation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: add a provider preflight requirement for MyPrivateAgent-compatible binding checks.

## Impact

- Affected code: provider contract models, provider service/router, health/capabilities helpers, smoke service, focused tests, README, OpenSpec spec.
- API: adds `GET /api/provider/preflight`.
- Dependencies: no new dependency, hosted model, vector database, queue, graph runtime, or MyPrivateAgent-side code.
