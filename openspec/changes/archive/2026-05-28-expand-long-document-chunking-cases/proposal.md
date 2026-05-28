## Why

The local Qdrant+BGE-M3 threshold recommendation now favors `0.7`, but current source fixtures are short paragraph-level chunks. Enterprise documents are often longer and contain multiple procedural details in one section, so we need benchmark evidence that checks whether the candidate threshold still preserves real recall on longer chunks.

## What Changes

- Add longer Chinese source paragraphs that simulate dense policy/procedure sections.
- Add benchmark cases that target details inside those longer sections.
- Preserve stable business citations for the new long-document chunks.
- Regenerate fixture and Qdrant+BGE evidence so threshold recommendation remains grounded in the expanded benchmark.

## Capabilities

### New Capabilities

### Modified Capabilities
- `retrieval-benchmark-harness`: add long-document chunking stress cases to the Chinese seed benchmark.
- `document-rag`: extend local Qdrant markdown citation anchors for added source paragraphs.

## Impact

- Affected fixtures: `app/data/sources/*.md`, `tests/fixtures/retrieval_benchmark_cases.json`.
- Affected code: fixture retriever source chunks and local Qdrant citation mapping.
- Affected docs/evidence: README and Chinese seed benchmark reports.
- No default threshold change, no production chunker change, no new dependency.
