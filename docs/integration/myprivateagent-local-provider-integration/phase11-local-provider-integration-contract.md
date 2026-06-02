# Phase 11 Local Provider Integration Contract

## Purpose

This contract defines a provider-side, read-only dry-run for MyPrivateAgent local integration.

It validates discovery, retrieval-consumption evidence, and source-binding preview compatibility before repository-side runtime integration.

## Local Assumptions

- Recommended local base URL: `http://127.0.0.1:8020`
- Local testing can keep `PROVIDER_API_KEY` unset.
- If API guard is enabled later, accepted headers remain:
  - `Authorization: Bearer <token>`
  - `X-Provider-Api-Key: <token>`

## Required Dry-Run Evidence

1. Phase 11 local integration profile export
2. Phase 11 provider discovery smoke
3. Phase 11 RAG retrieve consumption smoke
4. Phase 11 source-binding preview smoke

## Expected Boundaries

- `knowledge.graph.query` remains planned boundary.
- Runtime defaults remain unchanged (`keep_runtime_defaults`).
- Source binding stays preview-only in this phase.
- Source-to-agent binding decisions remain caller-owned.
- Registration, heartbeat governance, audit policy, and final answer policy remain caller-owned.

## Non-Goals

- No MyPrivateAgent repository code changes.
- No runtime promotion switch.
- No GraphRAG execution.
- No source-to-agent binding mutation.
