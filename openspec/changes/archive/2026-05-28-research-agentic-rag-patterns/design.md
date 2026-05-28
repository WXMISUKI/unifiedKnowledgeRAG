# Design: Agentic RAG Pattern Research

## Intent

This change turns external learning into an internal decision aid. It should help us avoid two common mistakes:

- Copying a mature framework's surface API before we know which retrieval failure we are solving.
- Building GraphRAG or reranking too early while the document ingestion and benchmark evidence are still maturing.

## Source Families

The research note will use public, mature sources from these families:

- LlamaIndex: agentic RAG patterns, query tools, routing, query transformations, sub-question retrieval.
- LangGraph: retrieval agents that decide whether to retrieve, grade evidence, rewrite queries, and loop.
- OpenAI Retrieval/File Search: vector stores, file ingestion, chunking, ranking options, and score thresholds.
- Microsoft GraphRAG: Local Search, Global Search, DRIFT Search, community/entity reasoning.
- Qdrant: hybrid search, dense/sparse vectors, filtering, and reranking patterns.

## Mapping Model

Each pattern is mapped into:

- `problem`: the retrieval or agent failure mode it addresses.
- `fit`: how well it fits `unifiedKnowledgeRAG`.
- `implementation stage`: now, next, later, or avoid-for-now.
- `evidence gate`: what benchmark evidence should exist before implementation.
- `dependency risk`: runtime dependency, service dependency, model dependency, or ops dependency.

## Current Architecture Alignment

The provider should continue to separate responsibilities:

```text
MyPrivateAgent
  - agent identity
  - policy and permissions
  - tool/capability orchestration
  - audit and governance

unifiedKnowledgeRAG
  - source catalog
  - ingestion lifecycle
  - document RAG retrieval
  - vector/embedding/rerank adapters
  - future GraphRAG data plane
```

Agentic retrieval loops should therefore be expressed as provider capabilities and evidence contracts first, not as a hard dependency on a specific agent framework.

## Recommended Near-Term Order

1. Keep improving document ingestion and chunking evidence.
2. Add query rewrite / evidence grading as benchmarked service-level helpers.
3. Add hybrid retrieval only if dense-only BGE-M3 misses exact-term or identifier-heavy cases.
4. Add reranker only after retrieval candidates produce noisy top-k evidence.
5. Add GraphRAG storage after a first relationship-heavy use case is defined.

## Validation

This change is validated by:

- OpenSpec strict validation.
- Linkable docs and specs.
- No runtime code path changes.
