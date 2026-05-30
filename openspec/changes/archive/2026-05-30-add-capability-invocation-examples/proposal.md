## Why

MyPrivateAgent can now discover and preflight-bind this provider, but it still has to infer request payloads from schemas or hardcoded knowledge. Adding machine-readable invocation examples makes the provider easier to bind, smoke-test, and integrate without changing runtime behavior.

## What Changes

- Extend capability invocation metadata with provider-owned example request payloads.
- Add examples for document retrieval, cited answer orchestration, and planned graph query boundaries.
- Validate examples through the provider contract smoke path so stale examples are caught early.
- Document the capability examples as integration hints, not production infrastructure choices.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: capability invocation metadata will include stable example request payloads for supported knowledge capability ids.

## Impact

- Affects `GET /api/capabilities` response shape by adding optional `invocation.example_request`.
- Affects provider contract smoke evidence and tests.
- Does not add dependencies, start external services, rebuild indexes, or choose embedding/vector/graph infrastructure.
