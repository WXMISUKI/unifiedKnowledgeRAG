# Design: RAG retrieval trace metadata

## Overview

`retrieval_trace` is a compact provider-owned diagnostic object for successful retrieval work. It complements `request_filter_context` and `answer_trace`.

## Trace Shape

The trace includes:

- `trace_id`: deterministic local trace id.
- `version`: retrieval trace contract version.
- `backend`: retrieval backend name.
- `requested_source_ids`: requested source scope.
- `top_k`: requested retrieval limit.
- `document_count`: returned document count.
- `citations`: returned citation ids.
- `score_summary`: min/max score when documents are returned.
- `filter_context`: the normalized request filter metadata.

## Answer Integration

The answer endpoint will attach the same `retrieval_trace` to answer metadata before evidence gating and finalization. `answer_trace` remains the answer decision trace; `retrieval_trace` is the retrieval diagnostic trace.

## Compatibility

The change is additive. Existing callers can ignore the new metadata.
