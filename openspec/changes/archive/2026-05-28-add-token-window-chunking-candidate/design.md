# Design: Token Window Chunking Candidate

## Strategy

`token-window-v1` is an evaluation candidate that chunks normalized markdown body text into overlapping windows using a lightweight deterministic tokenizer.

The tokenizer is intentionally simple for this slice:

- Chinese Han characters are treated as individual units.
- ASCII letter/digit runs are grouped as one unit.
- Punctuation and whitespace are separators unless needed to reconstruct readable text.

This avoids adding a production tokenizer dependency before we have benchmark evidence.

## Candidate Defaults

- `max_tokens`: 120
- `overlap_tokens`: 24
- `min_tokens`: 12

The values are conservative for the small local seed and can be revisited with real enterprise documents. The implementation should expose parameters on the pure chunking function so tests can use smaller windows.

## Citation Semantics

Token-window chunks should preserve provider-owned source/document identity:

- `source_id`
- `document_id`
- `title`
- `chunk_id`
- `citation`
- `chunking_strategy`

Known local sources may use deterministic token-window citation anchors. Unknown sources fall back to `document_id#token-window-N`.

This keeps citation behavior explicit and avoids rewriting benchmark expectations to make a candidate look better.

## Runtime Boundary

Default runtime Qdrant ingestion remains `markdown-paragraph-v1`. Token-window is used only when explicitly selected by local evaluation helpers or smoke comparison.

## Evidence

The checked-in evidence should include paragraph, section, and token-window strategies in:

```text
docs/benchmark/chinese-seed/chunking-candidates/qdrant-bge-m3-chunking-comparison.json
docs/benchmark/chinese-seed/chunking-candidates/qdrant-bge-m3-chunking-comparison.md
```

## Validation

- Focused chunking and benchmark tests.
- Full pytest suite.
- OpenSpec change validation.
- Main spec validation after archive.
