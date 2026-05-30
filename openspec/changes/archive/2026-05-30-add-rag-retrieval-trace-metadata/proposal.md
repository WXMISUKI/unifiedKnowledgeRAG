# Change: Add RAG retrieval trace metadata

## Why

`POST /api/rag/answer` now exposes answer trace metadata, and provider errors expose machine-readable details. Direct retrieval calls through `knowledge.rag.retrieve` still only return documents plus filter context. That leaves MyPrivateAgent and operators without a compact machine-readable summary of which backend ran, what source scope was requested, how many documents were returned, and which citations were considered.

This change adds retrieval trace metadata for retrieval-only diagnostics and reuses the same trace in answer metadata so retrieval and answer decisions can be correlated.

## What Changes

- Add provider-owned `retrieval_trace` metadata for successful RAG retrieval.
- Include backend, requested sources, top-k, document count, returned citations, score summary, and filter enforcement metadata.
- Include the same retrieval trace in answer metadata before answer finalization.
- Preserve existing retrieval and answer response contracts.

## Non-Goals

- No distributed tracing backend or OpenTelemetry integration.
- No raw vector scores beyond compact score summary.
- No retrieval ranking, chunking, or backend behavior changes.
- No persistence of traces outside the response envelope.
