## Why

unifiedKnowledgeRAG is intended to be a componentized external knowledge provider for MyPrivateAgent, but callers currently need to combine README knowledge, `/health`, `/api/capabilities`, and smoke evidence to understand provider identity and compatibility. A machine-readable integration manifest gives the control plane a stable preflight surface for service identity, contract version, supported capabilities, and integration endpoints.

## What Changes

- Add a read-only provider integration manifest endpoint.
- Include provider identity, contract version, component role, compatible control-plane hint, OpenAPI path, health path, capabilities path, smoke evidence paths, and capability ids.
- Keep public RAG, graph, ingestion, and index lifecycle contracts unchanged.
- Add focused contract tests and README documentation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: add a provider integration manifest requirement for MyPrivateAgent-compatible module discovery and preflight checks.

## Impact

- Affected code: contract models, new/read-only router or service, app wiring, provider contract tests, smoke checks, README, OpenSpec spec.
- API: adds `GET /api/provider/manifest`.
- Dependencies: no new dependency, database, queue, vector store, model, or graph runtime.
