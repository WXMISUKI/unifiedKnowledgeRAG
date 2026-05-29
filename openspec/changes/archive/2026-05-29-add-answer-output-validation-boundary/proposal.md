## Why

The provider now owns prompt packaging and rendering, but future hosted/local composers still need a shared output validation boundary. Before integrating an LLM, answers should be checked against allowed citations so unsupported or hallucinated citations can fail closed consistently.

## What Changes

- Add a deterministic answer output validator for cited answers.
- Validate that answered citations are non-empty and are a subset of prompt-package allowed citations.
- Attach output validation metadata to answered results.
- Keep deterministic answer behavior unchanged when validation passes.
- Do not call any external model or parse free-form LLM output in this change.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds answer output validation metadata and citation guardrails for cited answers.

## Impact

- Runtime: validates deterministic composer output through a provider-owned boundary.
- Contracts: enriches answer metadata with output validation details.
- Tests: verifies validation passes for deterministic answers and blocks invalid citations at the service boundary.
- Docs: updates README answer composer notes.
