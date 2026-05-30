# Change: Add provider error details

## Why

Provider errors currently expose stable `code` and human-readable `message`, but callers still need to parse message strings to identify unknown sources, not-ready indexes, unsupported composer configuration, or planned GraphRAG execution. That is brittle for MyPrivateAgent control-plane routing, governance UI, retries, and operator diagnostics.

This change adds machine-readable error details while preserving the existing error envelope.

## What Changes

- Add optional `details` to `ProviderError`.
- Populate details for unknown source and index-not-ready RAG errors.
- Populate details for unsupported or not-yet-implemented answer composer errors.
- Populate details for GraphRAG planned/not-implemented errors.
- Keep existing `code` and `message` values compatible.

## Non-Goals

- No HTTP status code changes.
- No exception middleware or global error handling rewrite.
- No authentication or authorization error taxonomy.
- No persistence or external tracing integration.
