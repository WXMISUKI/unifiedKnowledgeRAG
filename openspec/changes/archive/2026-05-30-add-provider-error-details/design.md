# Design: Provider error details

## Overview

`ProviderError.details` is an additive dictionary for machine consumers. It complements the stable `code` and human-readable `message`.

## Initial Details

RAG unknown source errors include:

- `requested_source_ids`
- `unknown_source_ids`

RAG index readiness errors include:

- `requested_source_ids`
- `not_ready_source_ids`
- `retrieval_backend`

Answer composer errors include:

- `configured_composer`
- `configured_model`
- `supported_composers`

GraphRAG not implemented errors include:

- `graph_id`
- `status`
- `capability_id`

## Compatibility

Existing clients can ignore `details`. Existing `ok=false`, `result=null`, `error.code`, and `error.message` semantics remain unchanged.
