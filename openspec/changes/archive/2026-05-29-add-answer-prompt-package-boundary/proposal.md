## Why

The answer composer boundary is ready for future hosted or local LLM adapters, but the prompt/evidence packaging rules are still implicit in the deterministic composer. Before integrating Qwen or a local model, the provider needs a stable prompt package boundary that carries evidence, citation constraints, and answer instructions consistently.

## What Changes

- Add an internal cited-answer prompt package builder.
- Include prompt package metadata in answered results so callers can audit which prompt policy shaped the answer.
- Pass query text into the composer boundary so future LLM adapters can build model prompts without changing the endpoint contract.
- Preserve deterministic answer text, evidence gate behavior, and fail-closed hosted/local composer behavior.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds prompt package metadata and query-aware answer composition boundary for cited answers.

## Impact

- Runtime: adds prompt package construction for answered results.
- Contracts: enriches answer metadata without changing top-level response shape.
- Tests: verifies prompt package id, citation policy, and allowed citations in answered metadata.
- Docs: updates README answer composer notes for prompt packaging.
