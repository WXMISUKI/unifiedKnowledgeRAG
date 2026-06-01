# Phase 8 Live URL Validation Execution Contract

- Report: `phase8-live-url-validation-execution-contract-v1`
- Status: `review`
- Scope: `deployed live URL validation execution`
- Generated At: `2026-06-01`

## Purpose

This contract defines how to execute live URL validation after deployment while preserving the lightweight provider boundary.
It is execution-oriented but read-only. It does not promote runtime defaults.

## Execution Inputs

Required inputs:

1. deployed provider `base_url`
2. provider route reachability to read-only endpoints

Optional input:

1. `PROVIDER_API_KEY` when protected `/api/*` access is enabled

## Allowed Endpoint Scope

Live URL validation should only call these read-only endpoints:

1. `GET /health`
2. `GET /api/provider/manifest`
3. `GET /api/provider/preflight`
4. `GET /api/provider/source-bindings`
5. `GET /api/provider/handoff`

## Status Semantics

| Status | Meaning |
| --- | --- |
| `ready` | live smoke ran against a real URL and required endpoint checks passed |
| `review` | live smoke is missing, partial, or needs reviewer judgment |
| `blocked` | live smoke failed hard or required inputs are invalid/missing |

Interpretation rules:

1. `ready` means live URL validation evidence is available.
2. `ready` does not mean runtime default promotion is approved.
3. `review` is expected before a real deployed URL exists.

## Non-Goals

1. runtime default promotion for Qdrant/BGE-M3/hybrid
2. ingestion, reindex, or graph execution
3. source-to-agent binding mutation
4. replacing control-plane registration, audit, or policy workflows
