# Change: research-agentic-rag-patterns

## Summary

Create a project-owned research note that compares mature Agentic RAG, Retrieval, GraphRAG, hybrid search, and reranking patterns, then map those patterns to `unifiedKnowledgeRAG` implementation priorities.

## Why

The provider already has a stable contract baseline, Qdrant+BGE-M3 local smoke evidence, score threshold evidence, and chunking comparison evidence. The next decisions involve agentic retrieval loops, query rewriting, reranking, hybrid retrieval, multi-granularity chunking, and GraphRAG search modes. Those decisions affect architecture, dependencies, benchmark gates, data residency, and operations.

We need a grounded internal reference before adding another runtime dependency or major retrieval behavior.

## Scope

In scope:

- Summarize mature public design patterns from LlamaIndex, LangGraph, OpenAI Retrieval/File Search, Microsoft GraphRAG, and Qdrant.
- Map each pattern to this provider's current architecture and benchmark evidence workflow.
- Classify each candidate pattern as `now`, `next`, `later`, or `avoid-for-now`.
- Update the production indexing architecture decision with the recommended near-term order.
- Add OpenSpec requirements that future RAG/GraphRAG implementation changes must reference the research note or fresher evidence.

Out of scope:

- Adding LangChain, LangGraph, LlamaIndex agent runtime, Neo4j, reranker, or hybrid retrieval runtime dependencies.
- Changing default Qdrant ingestion or retrieval behavior.
- Implementing GraphRAG storage.
- Replacing current benchmark cases.

## Expected Outcome

- `docs/research/agentic_rag_patterns.md` exists and is suitable as an architecture reference.
- Main specs require mature-pattern review before implementing agentic RAG, reranking, hybrid retrieval, or GraphRAG storage.
- README and architecture docs point future changes to the research note.
- No runtime behavior changes.
