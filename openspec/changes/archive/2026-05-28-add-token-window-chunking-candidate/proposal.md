# Change: add-token-window-chunking-candidate

## Summary

Make `token-window-v1` a runnable chunking strategy candidate for Chinese-heavy enterprise documents and include it in Qdrant+BGE-M3 chunking comparison evidence.

## Why

Recent evidence shows:

- `markdown-paragraph-v1` remains strong on the current Chinese seed, but may be too dependent on clean markdown paragraph boundaries.
- `markdown-section-v1` reduces chunk count but loses fine-grained citation match and some retrieval hits.
- Mature Agentic RAG research recommends improving document chunking evidence before introducing query rewrite, reranking, hybrid retrieval, or GraphRAG storage.

Enterprise corpora will include long policy text, PDF/Word extracted body text, pasted procedures, and dense Chinese paragraphs. We need a runnable token-window candidate before deciding whether to keep paragraph-only ingestion or move to multi-granularity indexing.

## Scope

In scope:

- Add a deterministic `token-window-v1` local chunking candidate.
- Preserve stable citation metadata and source/document identity.
- Include token-window chunks in local chunking strategy evaluation.
- Allow Qdrant+BGE-M3 smoke comparison to include paragraph, section, and token-window strategies.
- Export updated local evidence and document the result.

Out of scope:

- Switching default runtime Qdrant ingestion away from `markdown-paragraph-v1`.
- Adding a production tokenizer dependency.
- Adding PDF/Word parsing.
- Adding reranking, hybrid retrieval, query rewrite, or GraphRAG storage.

## Expected Outcome

- `token-window-v1` is marked runnable in candidate evidence.
- Smoke comparison can run all three strategies.
- README and specs record the candidate and its evidence.
- Runtime defaults remain unchanged.
