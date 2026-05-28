# Change: cache-bge-m3-local-model-artifact

## Summary

Add a repeatable local BGE-M3 model download and validation workflow, then cache the model artifact outside git for local and future private-network deployment.

## Motivation

The project now has an opt-in BGE-M3 local embedding adapter, but local and enterprise deployments still need the model files prepared ahead of time. Downloading at runtime is fragile, especially in private-network environments. We need a controlled bootstrap script, local manifest, git hygiene, and documentation so the model can be downloaded once and reused later.

## Goals

- Add a script that downloads `BAAI/bge-m3` into `models/bge-m3` by default.
- Support `HF_ENDPOINT` / mirror configuration without hard-coding a mirror as the default.
- Support local validation of required files and emit a manifest for deployment handoff.
- Ignore local model artifacts in git while keeping the workflow documented.
- Download the model into the local workspace for immediate use if network access succeeds.

## Non-Goals

- Do not commit model binaries.
- Do not implement sparse/hybrid retrieval or reranking.
- Do not switch the default embedding provider.
- Do not require network access during tests.
