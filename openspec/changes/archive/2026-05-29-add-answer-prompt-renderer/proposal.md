## Why

The provider now builds a cited-answer prompt package, but future hosted/local composers still do not have a stable rendered prompt shape to consume. Adding a deterministic renderer makes the next LLM integration safer without choosing a model provider yet.

## What Changes

- Add a renderer that turns a prompt package into provider-owned chat-style messages.
- Keep rendered prompt content internal, while exposing compact render metadata in answered results.
- Preserve answer text, evidence gate behavior, and fail-closed hosted/local composer behavior.
- Avoid external model calls or provider-specific prompt dependencies.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds deterministic prompt rendering metadata for cited answer prompt packages.

## Impact

- Runtime: adds prompt package rendering before deterministic answer composition.
- Contracts: enriches answer metadata with prompt renderer id and message count.
- Tests: verifies renderer metadata and prompt package citation alignment.
- Docs: updates README answer composer notes.
