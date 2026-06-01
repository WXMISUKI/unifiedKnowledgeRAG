# Phase 10 MyPrivateAgent Local Consumer Verification Contract

## Purpose

This contract defines the provider-side local verification slice that a MyPrivateAgent-shaped consumer can use before real MyPrivateAgent repository integration.

It is read-only local evidence. It does not change runtime defaults, create source-to-agent bindings, register the provider, implement GraphRAG execution, or move control-plane policy into this provider.

## Local Access Assumptions

- Recommended local base URL: `http://127.0.0.1:8020`
- Local development may leave `PROVIDER_API_KEY` unset.
- If `PROVIDER_API_KEY` is configured later, the caller should send one of:
  - `Authorization: Bearer <token>`
  - `X-Provider-Api-Key: <token>`
- `GET /health` remains public for component health checks.

## Required Read-Only Consumer Flow

The consumer verification flow should inspect these provider-owned surfaces:

1. `GET /health`
2. `GET /api/provider/manifest`
3. `GET /api/provider/preflight`
4. `GET /api/provider/source-bindings`
5. `GET /api/provider/handoff`

The flow may also use existing local evidence-pack smoke outputs to verify safe caller consumption of retrieval and cited-answer envelopes. It should not create bindings, mutate sources, rebuild indexes, run ingestion, download models, call vector stores directly, or execute GraphRAG.

## Expected Consumer Signals

| Signal | Expected Local Meaning |
|---|---|
| local provider URL | `http://127.0.0.1:8020` unless a later deployment explicitly supplies another base URL |
| API key mode | `not_configured_local_dev` is acceptable for local testing |
| provider manifest | provider identity, contract version, supported capabilities, endpoint paths, and access metadata are discoverable |
| provider preflight | bindability and review notes are machine-readable |
| source binding review | source readiness can be inspected, but binding decisions remain caller-owned |
| handoff bundle | local evidence can be reviewed through one provider-owned artifact |
| evidence pack readiness | caller can fail closed when provider evidence is insufficient |
| graph boundary | `knowledge.graph.query` remains planned, not executable |
| runtime promotion | Qdrant, BGE-M3, hybrid, aggregation, and relation-aware grading remain behind evidence gates |

## Ownership Boundary

This provider owns evidence, citations, diagnostics, read-only source readiness, and handoff metadata.

MyPrivateAgent or another caller owns:

- provider registration,
- heartbeat governance,
- user identity and authorization policy,
- source-to-agent binding decisions,
- approval and audit workflows,
- final user-facing answer style,
- final orchestration and tool execution.

## Non-Goals

- No MyPrivateAgent repository changes.
- No runtime default promotion.
- No GraphRAG execution.
- No source-to-agent binding mutation.
- No production private-network certification.
