## Why

`/api/capabilities` now lists retrieval, answer, and graph capability ids, but callers still need out-of-band knowledge to invoke them. Adding minimal invocation metadata makes the provider more useful to MyPrivateAgent and other orchestrators without forcing a larger capability registry redesign.

## What Changes

- Add optional machine-readable invocation metadata to capability entries.
- Include HTTP method and path for RAG retrieval, RAG answer, and graph query capability ids.
- Preserve existing capability id, status, and description fields.
- Keep richer schema, auth, and policy metadata out of scope for this small slice.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Adds endpoint invocation metadata to stable provider capabilities.

## Impact

- API: enriches `GET /api/capabilities` response with optional invocation metadata.
- Contracts: adds a small capability invocation model.
- Tests: verifies the answer and retrieval capabilities expose method/path metadata.
- Docs: updates README capability discovery notes.
