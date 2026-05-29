## Why

The answer endpoint now has a deterministic cited response and evidence gate, but the composer is still a hard-coded function. Before integrating Qwen, OpenAI, or a local LLM, the provider needs a stable composer boundary so model choices remain explicit, testable, and fail-closed.

## What Changes

- Introduce a provider-neutral answer composer adapter interface.
- Add configurable composer selection through provider settings.
- Keep `deterministic` as the default composer and preserve current answer behavior.
- Add fail-closed placeholders for hosted and local LLM composers until a model decision is approved.
- Include composer provider metadata in answer responses for audit and future compatibility.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds configurable answer composer provider selection and fail-closed unsupported composer behavior.

## Impact

- Configuration: adds `RAG_ANSWER_COMPOSER` and optional model metadata settings.
- Runtime: replaces direct deterministic composition with an adapter factory.
- API: preserves endpoint shape while enriching answer metadata.
- Tests: covers deterministic default behavior and unsupported composer failure.
- Docs: documents the composer boundary and why hosted/local models are not enabled yet.
