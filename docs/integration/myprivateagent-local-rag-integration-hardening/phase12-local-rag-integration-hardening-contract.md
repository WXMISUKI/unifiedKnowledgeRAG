# Phase 12 Local RAG Integration Hardening Contract

## Purpose

This contract defines a local hardening slice for MyPrivateAgent-style RAG integration, after Phase 11 local provider integration.

Phase 12 is a read-only hardening phase. It focuses on operational readiness and evidence alignment before any runtime promotion work.

## Local Assumptions

- Recommended local base URL: `http://127.0.0.1:8020`
- For local development, `PROVIDER_API_KEY` can be kept unset.
- If enabled later, local API access follows existing key patterns:
  - `Authorization: Bearer <token>`
  - `X-Provider-Api-Key: <token>`

## Required Evidence

To enter Phase 12 hardening readiness/smoke, the following artifacts are required:

1. Phase 10 local consumer verification readiness
2. Phase 10 local consumer probe
3. Phase 11 local provider integration profile
4. Phase 11 source-binding preview smoke
5. Phase 11 rag-retrieve consumption smoke
6. Provider contract smoke
7. Provider handoff bundle

## Hardening Checks

`build_phase12_local_rag_integration_hardening_smoke` validates:

- phase12 local hardening profile presence,
- provider contract smoke pass,
- provider integration manifest check from contract smoke,
- handoff artifact row consistency against required evidence,
- source-binding preview readiness,
- retrieval consumption readiness.

## Non-Goals

- No runtime default promotion (`keep_runtime_defaults` remains).
- No GraphRAG execution changes.
- No MyPrivateAgent repository code changes in this phase.
- No source-to-agent binding mutation.
- No candidate backend promotion (Qdrant, BGE-M3, hybrid, etc.).

## Ownership Boundary

- Contract/runtime defaults remain caller-owned for policy and binding decisions.
- This project only owns provider-side evidence and hardening checks.
