## Why

Capabilities now expose method and path, but callers still need external knowledge to construct request bodies and parse responses. Adding schema references makes capability discovery more actionable for MyPrivateAgent without introducing a full tool registry.

## What Changes

- Add optional request and response schema references to capability invocation metadata.
- Use OpenAPI component references for retrieval, answer, and graph query capabilities.
- Preserve existing capability ids, status, description, and method/path metadata.
- Keep auth policy, examples, rate limits, and rich tool manifests out of scope.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Adds request/response schema references to capability invocation metadata.

## Impact

- API: enriches `GET /api/capabilities` with schema refs under `invocation`.
- Contracts: extends `CapabilityInvocation` with optional schema reference fields.
- Tests: verifies RAG answer and retrieval capabilities expose request/response schema refs.
- Docs: updates README capability discovery notes.
