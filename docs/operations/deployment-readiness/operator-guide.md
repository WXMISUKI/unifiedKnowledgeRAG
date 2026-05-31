# Deployment Readiness Operator Guide

This guide explains how to read the current deployment readiness evidence and what to do before treating the provider as deployable. It is intentionally operational, not policy-driven.

## Current Snapshot

The current `deployment-readiness-v1` report is `review`, which means the provider is healthy enough for local development and binding review, but it is not yet ready for deployment promotion.

The main reasons are:

- `embedding_provider` is still `mock`
- `rag_retrieval_backend` is still `fixture`
- `Qdrant` is configured but not yet treated as the promoted deployment backend
- `model_artifacts` are not configured
- `PROVIDER_API_KEY` is not configured
- `deployed_provider_smoke` is optional and currently missing because there is no live base URL evidence

## What `review` Means

`review` does not mean the code is broken. It means the current local evidence is honest about the remaining deployment work.

Use this state to continue development locally, but do not treat the component as deployment-ready until the preconditions below are satisfied.

## Pre-Deployment Checklist

Before deployment, confirm the following:

- Choose a real embedding candidate instead of `mock`
- Decide whether the deployment backend uses Qdrant or stays fixture-based for local-only work
- Configure a model artifact directory when using a local embedding model
- Mount or publish the source and index directories required by the runtime
- Set `PROVIDER_API_KEY` when exposing `/api/*` outside trusted local development
- Regenerate readiness evidence after any configuration change

## Current Evidence Fields

The readiness export currently surfaces these signals:

| Field | Meaning |
|---|---|
| `health.status` | Overall provider process health |
| `preflight.bindable` | Whether the provider can be bound by an external control plane |
| `contract_smoke.passed` | Whether the local contract smoke evidence is passing |
| `runtime_config.embedding_provider` | Current embedding mode |
| `runtime_config.rag_retrieval_backend` | Current retrieval backend |
| `runtime_config.provider_api_key_configured` | Whether API access protection is enabled |
| `model_artifacts.status` | Whether a local model artifact is configured |

## Standard Commands

Run these commands when you need to refresh local evidence:

```powershell
python scripts/export_deployment_readiness.py
python scripts/export_reindex_readiness.py
python scripts/export_provider_handoff_refresh.py
```

Use deployed smoke only after a live provider base URL exists:

```powershell
python scripts/export_deployed_provider_smoke.py --base-url http://127.0.0.1:8020
```

## How To Read The Results

- `deployment-readiness.json` tells you whether the component is locally ready for deployment planning.
- `reindex-readiness.json` tells you whether source freshness and index state are acceptable.
- `provider-handoff-refresh.json` is the recommended maintenance output because it regenerates the supporting evidence in order.
- `deployed-provider-smoke.json` is optional until there is a real deployed URL to target.

## Boundary Notes

- The provider does not own registration, heartbeat governance, audit policy, or source-to-agent binding decisions.
- The guide does not promote Qdrant, BGE-M3, or any hybrid retrieval candidate to runtime default.
- The guide does not add deployment automation; it only makes the current operator path explicit.

## Maintenance

When runtime configuration or source/index state changes, rerun:

```powershell
python scripts/export_provider_handoff_refresh.py
```

Treat the refreshed evidence as the source of truth for the next deployment review.
