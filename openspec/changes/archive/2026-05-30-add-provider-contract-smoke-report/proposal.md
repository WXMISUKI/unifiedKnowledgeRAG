## Why

The provider now exposes retrieval, cited answer, graph boundary, error details, and trace metadata, but callers still lack a single executable contract smoke report that proves those surfaces work together. Adding a local smoke report gives MyPrivateAgent and future deployment checks a stable way to verify basic provider usability before deeper RAG or GraphRAG optimization.

## What Changes

- Add a provider contract smoke runner that exercises health, capabilities, retrieval, answer, and planned graph query boundaries through the existing FastAPI contract.
- Add an export script that writes machine-readable JSON and a concise Markdown summary for local evidence review.
- Add focused tests for the smoke runner and report shape.
- Document the local smoke command in README.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: add a provider-owned executable contract smoke report requirement for local integration readiness evidence.

## Impact

- Affected code: new service module, new script, focused tests, README.
- Public HTTP APIs remain unchanged.
- No new runtime dependency, database, vector store, hosted model, or network call is introduced.
