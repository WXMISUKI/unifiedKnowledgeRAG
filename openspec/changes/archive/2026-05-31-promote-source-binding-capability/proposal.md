## Why

The provider already exposes a read-only source binding summary endpoint, but external control planes still cannot discover it as a formal capability from `/api/capabilities` or include it in preflight capability requirements. Promoting it to a capability makes the binding-review workflow API-native without moving source-to-agent binding policy into this provider.

## What Changes

- Add a formal capability id for source binding review metadata.
- Advertise the source binding summary endpoint, schema reference, and example request from `/api/capabilities`.
- Include the source binding capability in the provider manifest capability list and default preflight capability set.
- Document that this is read-only provider-owned evidence, not binding execution, approval, audit, or final answer policy.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Add source binding review as a discoverable provider capability.
- `provider-roadmap`: Mark source binding capability promotion as Phase 6 integration work that preserves the lightweight provider boundary.

## Impact

- Affected API contracts: `/api/capabilities`, `/api/provider/manifest`, `/api/provider/preflight`
- Affected code: provider capability catalog, manifest capability ids, preflight defaults, contract tests
- Affected docs/specs: README, lightweight provider roadmap, knowledge-provider spec, provider-roadmap spec
- No new runtime dependencies, persistence changes, ingestion execution, vector DB calls, GraphRAG execution, or MyPrivateAgent policy ownership changes
