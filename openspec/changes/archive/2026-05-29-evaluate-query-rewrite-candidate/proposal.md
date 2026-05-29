# Change: evaluate-query-rewrite-candidate

## Summary

Add a local query rewrite candidate evaluation workflow that compares original benchmark queries with controlled rewritten queries while preserving expected-empty cases and runtime retrieval defaults.

## Why

The latest chunking evidence shows that paragraph chunking still wins on citation match, while section and token-window candidates expose useful but insufficient trade-offs. Mature Agentic RAG patterns suggest the next safer improvement is query transformation evidence before adding rerankers, hybrid retrieval, or GraphRAG storage.

Query rewrite can improve paraphrased or shorthand enterprise questions, but it can also create false positives for unsupported questions. We need a local, benchmark-first gate before any runtime adoption.

## Scope

In scope:

- Define query rewrite candidates and a deterministic controlled rewrite policy.
- Evaluate candidates against the existing benchmark cases and selected retrieval backend.
- Export JSON and Markdown evidence.
- Preserve expected-empty cases and report rewrite coverage.
- Update docs/specs with the boundary that query rewrite is evaluation-only.

Out of scope:

- Calling hosted LLMs for query rewriting.
- Adding a query rewrite HTTP API.
- Enabling query rewrite in default runtime retrieval.
- Adding reranking, hybrid retrieval, or GraphRAG storage.

## Expected Outcome

- Query rewrite candidate evidence can be exported locally.
- Controlled rewrite coverage and benchmark metrics are visible.
- Runtime retrieval behavior remains unchanged.
