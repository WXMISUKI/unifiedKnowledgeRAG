# Phase 9 MyPrivateAgent Local Consumption Contract

- Report: `phase9-myprivateagent-local-consumption-contract-v1`
- Status: `review`
- Scope: `myprivateagent local provider consumption`
- Generated At: `2026-06-01`

## Purpose

This contract defines how MyPrivateAgent consumes unifiedKnowledgeRAG in local development without crossing provider/control-plane boundaries.
It is read-only integration guidance and does not promote runtime defaults.

## Local Baseline

1. Recommended local provider URL: `http://127.0.0.1:8020`
2. Local development may keep `PROVIDER_API_KEY` unset.
3. If `/api/*` protection is enabled later, use either:
   - `Authorization: Bearer <token>`
   - `X-Provider-Api-Key: <token>`

## Required Read-Only Discovery Flow

MyPrivateAgent local consumption should start from:

1. `GET /health`
2. `GET /api/provider/manifest`
3. `GET /api/provider/preflight`
4. `GET /api/provider/source-bindings`
5. `GET /api/provider/handoff`

## Ownership Boundary

Provider-owned scope:

1. evidence, citations, diagnostics, and handoff artifacts
2. read-only source-binding readiness summaries
3. retrieval/answer and graph planned-boundary signals

MyPrivateAgent-owned scope:

1. source-to-agent binding policy and execution
2. user identity, RBAC/approval policy, and audit workflow
3. final answer policy and runtime governance

## Non-Goals

1. runtime default promotion for Qdrant/BGE-M3/hybrid
2. GraphRAG execution implementation
3. source-to-agent binding mutation from provider side
4. replacing caller control-plane governance workflows
