# Design: RAG request filter context

## Overview

The provider will normalize request `filters` into a compact filter context before retrieval. This gives downstream retrieval backends one stable object instead of each backend parsing arbitrary request dictionaries.

## Supported Keys

The first filter context supports:

- `tenant_id`: optional string.
- `document_ids`: optional list of strings.
- `acl_tags`: optional list of strings.
- `agent_id`: optional string for audit metadata.
- `role`: optional string for audit metadata.

Unknown filter keys are preserved in `extra_filters` for diagnostics but are not enforced by backends.

## Backend Behavior

- Qdrant uses `tenant_id`, `document_ids`, and `acl_tags` in its existing payload filter.
- Fixture and LlamaIndex keep current retrieval behavior and return metadata indicating filters were not enforced by that backend.

## Response Metadata

`POST /api/rag/retrieve` will include `result.metadata.request_filter_context`.

`POST /api/rag/answer` will include the same `request_filter_context` in answer metadata so the answer trace and audit metadata can be correlated with the caller's requested scope.

## Compatibility

The existing `answer_context` and `documents` fields remain unchanged. Adding result metadata to retrieval is additive and keeps existing callers compatible.
