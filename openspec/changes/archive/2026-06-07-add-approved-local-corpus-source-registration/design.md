## Overview

This change adds the smallest approved-source bridge between local trial artifacts and the provider's normal source surfaces. It treats caller handoff as an input gate, not as automatic registration.

The approved source flow is:

```text
local corpus caller handoff
  -> validate status=ready_for_caller_review
  -> copy markdown into app/data/sources/<source_id>.md
  -> write app/data/local_sources/approved_sources.json
  -> catalog / manifest / retrieve / answer can resolve source_id
```

## Design Decisions

### Explicit local registry

Approved local sources are stored in `app/data/local_sources/approved_sources.json`. This keeps the feature lightweight and reversible: deleting the registry entry and copied markdown removes the approved local source from provider discovery.

The registry stores only provider-owned facts needed to run locally:

- `source_id`
- `title`
- `owner`
- `version`
- `domain`
- `language`
- `sensitivity`
- `source_path`
- `document_id`
- `citation_prefix`
- `registration_status`
- `handoff_path`

### Handoff remains a gate

Only handoffs with `status=ready_for_caller_review` and `registration_status=not_registered` can be registered. Review, blocked, malformed, or missing handoffs produce a blocked registration result.

### Provider-visible, not caller-bound

The registration makes the source visible to provider-owned source discovery and retrieval. It does not create a source-to-agent binding, approval workflow, audit event, or MyPrivateAgent runtime state.

### Retrieval support

The default fixture retriever is extended to read approved local markdown chunks in addition to built-in fixture chunks. This keeps day-1 local usage simple without requiring Qdrant/BGE setup. LlamaIndex already reads `settings.rag_source_dir / <source_id>.md`; its metadata fallback is kept compatible with dynamic approved sources.

### Manifest and package support

`source_catalog`, `source_package`, and `source_document_manifest` merge built-in source metadata with approved local registry entries. Dynamic manifests use markdown chunk fallback citations such as `<document_id>#chunk-1`.

## Non-Goals

- No raw PDF ingestion support.
- No OCR or PaddleOCR service startup.
- No formal ingestion job creation.
- No index lifecycle promotion.
- No Qdrant/BGE/hybrid/reranker runtime promotion.
- No source-to-agent binding.
- No MyPrivateAgent orchestration.
- No GraphRAG execution.
