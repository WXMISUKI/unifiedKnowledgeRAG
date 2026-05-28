## Why

The Qdrant + BGE-M3 smoke path now runs end-to-end, but citation match is still low because Qdrant ingestion emits generic `chunk-N` citations while the benchmark cases expect stable business anchors such as `refund_policy_2026#section-3` and `logistics_faq_2026#lost-package`.

Before evaluating rerankers or hybrid retrieval, Qdrant ingestion needs a deterministic citation strategy for local markdown sources so benchmark evidence can distinguish a correct evidence hit from a merely correct source hit.

## What Changes

- Add source-specific citation anchors for the current local markdown fixture sources.
- Preserve generic chunk fallback for unknown sources or unmapped paragraphs.
- Keep point ids and chunk ids stable while using business citations in payloads.
- Re-run Qdrant + BGE-M3 smoke evidence and compare citation metrics.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `document-rag`: Qdrant markdown ingestion emits stable citation anchors for known local sources.
- `retrieval-benchmark-harness`: Qdrant smoke evidence can use business citation anchors for benchmark comparison.

## Impact

- Affects Qdrant markdown chunk metadata generation.
- Affects smoke evidence output.
- No new dependencies or public API changes.
