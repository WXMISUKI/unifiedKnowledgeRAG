# Agentic RAG Pattern Research

## Purpose

This note records mature Agentic RAG, Retrieval, GraphRAG, hybrid search, and reranking patterns, then maps them to the `unifiedKnowledgeRAG` roadmap.

It is a decision aid, not a dependency approval. Future changes that add query rewriting, retrieval grading, hybrid retrieval, reranking, or GraphRAG storage should reference this note or replace it with fresher benchmark evidence.

## Current Project Baseline

The provider currently has:

- Provider-neutral HTTP contracts for document RAG and graph query boundaries.
- Explicit ingestion job lifecycle, durable local job/source status, retry, cancellation, stale recovery, retention, and a queued runner.
- Qdrant as the first vector-store candidate.
- BGE-M3 local dense embedding adapter.
- Qdrant+BGE smoke evidence, threshold sweep evidence, threshold recommendation evidence, and chunking comparison evidence.
- A Chinese-heavy benchmark seed with positive citation cases, long-section cases, and expected-empty cases.
- Local query rewrite candidate evidence that compares original queries with deterministic controlled rewrites.
- Local evidence grading candidate evidence that labels answer-bearing, insufficient, missing, and expected-empty outcomes.
- A dedicated evidence grading stress fixture that exposes related-insufficient, missing-evidence, and unexpected-evidence outcomes without replacing the main Chinese seed.

Current evidence says:

- `RAG_SCORE_THRESHOLD=0.7` is a good local seed candidate, not a production approval.
- `markdown-paragraph-v1` remains the safest current default.
- Pure `markdown-section-v1` reduces chunk count but loses fine-grained citation match and some hits.
- `controlled-support-rewrite-v1` rewrites selected non-empty seed cases without regressing fixture metrics, while preserving expected-empty cases.
- `citation-match-grader-v1` and `source-match-grader-v1` establish a local evidence grading shape, but harder insufficient-evidence cases are still needed before runtime answer gating.
- Evidence grading stress evidence shows strict citation grading can catch related-but-insufficient evidence that source-level grading would over-credit.

## Mature Pattern Families

| Source family | Mature pattern | What it optimizes | Project fit |
| --- | --- | --- | --- |
| LlamaIndex agentic strategies | Routing, query transformations, sub-question query engines, query-engine tools | Better query decomposition and tool selection before retrieval | Strong fit as a design model; do not copy runtime dependency yet |
| LangGraph retrieval agent | Decide whether to retrieve, grade retrieved documents, rewrite weak queries, loop to answer | Self-correcting retrieval flow | Strong fit for future service-level retrieval orchestration |
| OpenAI Retrieval/File Search | Vector stores, file ingestion, chunking strategy, ranking options, score threshold, hybrid search weights | Productized retrieval controls and ranking knobs | Strong fit for our evidence metadata and threshold workflow |
| Microsoft GraphRAG | Local Search, Global Search, DRIFT Search over graph indexes and text chunks | Relationship-heavy and global-summary questions | Later fit after a real graph use case is defined |
| Qdrant hybrid/reranking | Dense + sparse search, staged retrieval, late-interaction reranking | Improve recall and top-k precision while keeping fast coarse retrieval | Good candidate after dense-only misses identify exact-term or noisy-top-k problems |

References:

- [LlamaIndex Agentic Strategies](https://docs.llamaindex.ai/en/stable/optimizing/agentic_strategies/agentic_strategies/)
- [LlamaIndex Query Transformations](https://docs.llamaindex.ai/en/v0.10.17/optimizing/advanced_retrieval/query_transformations.html)
- [LangGraph Agentic RAG](https://docs.langchain.com/oss/python/langgraph/agentic-rag)
- [OpenAI Retrieval](https://platform.openai.com/docs/guides/retrieval)
- [Microsoft GraphRAG Query Overview](https://microsoft.github.io/graphrag/query/overview/)
- [Microsoft DRIFT Search](https://www.microsoft.com/en-us/research/blog/introducing-drift-search-combining-global-and-local-search-methods-to-improve-quality-and-efficiency/)
- [Qdrant Hybrid Search With Reranking](https://qdrant.tech/documentation/tutorials-basics/reranking-hybrid-search/)
- [Qdrant Hybrid Queries](https://qdrant.tech/documentation/concepts/hybrid-queries/)

## Pattern Mapping

### 1. Query Routing

Problem:

- Not every user query needs retrieval.
- Some queries should go to document RAG; future relationship-heavy queries may go to GraphRAG.

Fit:

- Very good for MyPrivateAgent + provider split.
- The agent control plane can decide which provider capability to invoke.
- The provider can also expose lightweight route metadata later, but should not own agent identity or permissions.

Adoption stage: `next`

Evidence gate:

- Add benchmark cases labeled by retrieval need: no-retrieval, document-rag, graph-rag-candidate, unsupported.
- Measure false retrieval and missed retrieval separately.

Dependency risk:

- Low if implemented as service-level classifier.
- Medium if tied to an agent framework runtime.

### 2. Query Rewrite / Transformation

Problem:

- User questions may be underspecified, paraphrased, or phrased in a way that embeds poorly.
- Chinese enterprise questions often contain shorthand, mixed terms, or incomplete business context.

Fit:

- Good after the chunking baseline is stable.
- Should be benchmarked as a candidate retrieval helper, not blindly enabled.

Adoption stage: `next`

Evidence gate:

- Add a candidate evaluation comparing original query vs rewritten query.
- Track hit rate, citation match rate, empty handling, and latency.
- Ensure rewrites do not turn expected-empty queries into false positives.

Dependency risk:

- Medium because it requires an LLM or deterministic rewrite policy.
- Data egress must be reviewed if hosted LLM rewriting is used.

### 3. Evidence Grading

Problem:

- Vector retrieval can return semantically close but not answer-bearing chunks.
- High score is not the same as grounded answerability.

Fit:

- Strong fit.
- LangGraph-style grade-then-answer is useful, but in this provider it should become an evidence quality gate or local evaluation helper first.

Adoption stage: `next`

Evidence gate:

- Add per-case evidence labels: answer-bearing, related-but-insufficient, unsupported.
- Measure whether grading improves precision without hiding retrieval misses.

Dependency risk:

- Medium if LLM-based.
- Low for heuristic first pass, but heuristic value may be limited.

### 4. Multi-query / Sub-question Retrieval

Problem:

- Multi-intent or multi-hop questions may need several retrievals and merged evidence.

Fit:

- Good for complex support workflows.
- It should wait until single-query chunking and citation behavior are stable.

Adoption stage: `later`

Evidence gate:

- Add multi-intent benchmark cases with multiple expected citations.
- Track whether each expected citation is found, not just whether any source matches.

Dependency risk:

- Medium to high because query expansion increases latency and cost.

### 5. Hybrid Dense + Sparse Retrieval

Problem:

- Dense retrieval can miss exact terms, identifiers, policy numbers, SKU-like codes, form names, and business acronyms.
- Sparse retrieval can improve exact-term recall but may add noise.

Fit:

- Strong Qdrant candidate after dense-only misses appear.
- BGE-M3 can support future sparse/hybrid exploration, but current adapter intentionally emits only dense vectors.

Adoption stage: `later`, unless dense-only benchmark misses exact-term cases

Evidence gate:

- Add exact-term and identifier-heavy benchmark cases.
- Compare dense-only vs dense+sparse or dense+BM25.
- Track citation match and empty false positives, not only hit rate.

Dependency risk:

- Medium because it changes indexing schema and query fusion.
- Reindex migration must be planned.

### 6. Reranking

Problem:

- Retrieval may find the right document in top-k but rank weak evidence above answer-bearing evidence.

Fit:

- Good after candidate retrieval produces noisy top-k.
- Should not be the first response to chunking failures.

Adoption stage: `later`

Evidence gate:

- Capture top-k candidate sets before and after reranking.
- Require category-level improvement, especially citation match and long-section precision.

Dependency risk:

- Medium to high depending on reranker model, latency, and deployment path.

### 7. GraphRAG Local / Global / DRIFT Search

Problem:

- Document RAG is weak for entity relationships, cross-document joins, global summaries, and multi-hop reasoning over structured relations.

Fit:

- Architecturally important but not the next implementation slice.
- GraphRAG should remain separate from the document vector store.

Adoption stage: `later`

Evidence gate:

- Define the first relationship-heavy business use case.
- Add graph-specific benchmark cases with expected entities, relations, paths, and source citations.
- Decide whether graph answers cite source documents, business records, or both.

Dependency risk:

- High because it introduces graph storage, entity extraction, ontology/versioning, and reconciliation workflows.

## Recommended Roadmap

| Order | Work item | Why now |
| ---: | --- | --- |
| 1 | Exact-term / identifier benchmark cases | Required before deciding hybrid retrieval |
| 2 | Multi-granularity indexing candidate | Paragraph still wins on citation match, while section and token-window expose complementary recall/cost trade-offs |
| 3 | Dense+sparse hybrid candidate | Only after dense-only misses justify schema/query complexity |
| 4 | Reranker candidate | Only after top-k contains right evidence but poor ordering |
| 5 | Runtime query rewrite or evidence grading decision | Only after broader true/false positive evidence confirms safe promotion beyond deterministic local evidence |
| 6 | GraphRAG first use case and storage candidate | Only after relationship-heavy questions are concrete |

## Decisions For This Provider

- Keep `unifiedKnowledgeRAG` as the knowledge data plane.
- Keep MyPrivateAgent as the agent control plane and policy/runtime orchestrator.
- Do not add a full agent framework dependency just to implement Agentic RAG patterns.
- Treat each mature pattern as a candidate with benchmark evidence.
- Keep document RAG, hybrid retrieval, reranking, and GraphRAG as separate approval gates.
- Preserve citations as first-class evaluation outputs.
- Preserve expected-empty cases when adding query rewrite or agentic loops, because over-retrieval is a serious enterprise risk.

## Near-Term Recommendation

After insufficient-evidence stress cases are in place, the next implementation slice should be:

```text
expand-exact-term-identifier-benchmark-cases
```

It should add policy numbers, order-like ids, form names, and business acronyms so dense-only retrieval can be tested against cases that may need sparse or hybrid retrieval later.
