## Context

The local source markdown files are simple fixture documents. They do not include explicit anchor markers, but the benchmark seed already encodes stable citation expectations. Current Qdrant ingestion uses `document_id#chunk-N`, which is mechanically stable but not aligned with provider-owned citations used by existing fixture and LlamaIndex paths.

This change introduces a small deterministic mapping for known fixture sources only. It keeps the enterprise parser decision open while making benchmark evidence useful now.

## Goals / Non-Goals

**Goals:**

- Emit benchmark-compatible citations for known fixture paragraphs.
- Preserve chunk ids, point ids, source path, and chunking strategy metadata.
- Keep fallback behavior for unknown sources or paragraphs beyond the mapping.
- Improve Qdrant smoke citation match evidence without changing benchmark expectations.

**Non-Goals:**

- Do not implement a final enterprise document parser.
- Do not infer anchors from arbitrary markdown headings or semantic content.
- Do not change embedding, Qdrant query, thresholds, reranking, or graph behavior.

## Decisions

1. Use source-specific paragraph-index mappings.

   The current local fixture documents are stable, tiny, and already tied to benchmark evidence. A mapping by source id and paragraph ordinal is explicit, testable, and avoids brittle keyword parsing.

2. Keep `chunk_id` as `chunk-N`.

   Chunk ids represent the physical chunk position; citations represent external evidence anchors. Keeping both lets us audit chunking while returning business citations.

3. Preserve fallback `document_id#chunk-N`.

   Unknown sources and additional paragraphs still need deterministic citations. The fallback keeps behavior safe until a richer parser is designed.

## Risks / Trade-offs

- [Risk] Fixture-specific mapping is not production parsing. -> Mitigation: document it as local benchmark alignment only and keep production parser decisions separate.
- [Risk] Paragraph order changes can invalidate mappings. -> Mitigation: focused tests lock the fixture mapping and smoke evidence will surface regressions.
- [Risk] Citation match may still be imperfect due to ranking. -> Mitigation: this change only fixes citation identity; ranking remains a later reranker/chunking question.
