## Why

The provider now exposes `/api/rag/answer`, but `/api/capabilities` still advertises only document retrieval and graph query boundaries. Upper-layer agents need a stable capability id to discover cited answer orchestration without hard-coding endpoint knowledge.

## What Changes

- Add `knowledge.rag.answer` to the provider capability registry.
- Keep `knowledge.rag.retrieve` as the lower-level evidence retrieval capability.
- Document that answer capability remains provider-neutral and does not imply a hosted or local LLM is enabled.

## Capabilities

### New Capabilities

### Modified Capabilities
- `knowledge-provider`: Adds the stable `knowledge.rag.answer` capability id to provider capability discovery.

## Impact

- API: updates `GET /api/capabilities` response content without changing the response shape.
- Tests: updates provider contract tests for the new capability id.
- Docs: updates README capability list and answer capability notes.
