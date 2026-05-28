## Context

The current provider intentionally uses local files, MockEmbedding, and an explicit local queued runner. That has been useful for stabilizing provider-owned contracts and lifecycle behavior. The next production step is not simply "install a vector database"; it requires a set of connected architecture decisions.

The user explicitly requested that unclear choices such as embedding models and vector databases be discussed before implementation. This design therefore creates a decision framework rather than selecting final infrastructure.

## Goals / Non-Goals

**Goals:**

- Create a shared decision record for production indexing architecture.
- Separate reversible local implementation from production infrastructure choices.
- Identify candidate options and evaluation criteria.
- Define a decision gate before adding external provider dependencies.
- Keep the provider-neutral HTTP contract stable.

**Non-Goals:**

- No final embedding model choice in this change.
- No final vector database choice in this change.
- No new queue, worker, database, embedding, vector store, reranker, or graph driver dependency.
- No benchmark implementation yet.

## Decisions

1. Use a decision record before production dependency implementation.

   The project should not silently adopt a production embedding model, vector store, queue, or graph store through code changes. These affect operating cost, data residency, latency, recall, and deployment.

2. Evaluate vector stores by workload fit rather than popularity.

   Candidate families include PostgreSQL + pgvector for operational simplicity, Qdrant for dedicated vector/hybrid retrieval, Milvus for larger-scale vector workloads, and cloud-managed vector services if operational ownership should be minimized.

3. Keep dense, sparse, and hybrid retrieval as separate design choices.

   Hybrid retrieval can improve exact term matching plus semantic recall, but it changes indexing, query execution, and reranking requirements.

4. Treat GraphRAG storage as a parallel decision.

   Document RAG vector infrastructure and graph storage should not be collapsed. GraphRAG needs ontology, entity/relation lifecycle, graph storage, traversal, and evidence contracts.

## Risks / Trade-offs

- Delaying final vendor choices can feel slower -> mitigated by keeping local contracts moving while decision criteria are prepared.
- Too many options can block progress -> the decision record should narrow candidates to a short list after user review.
- Official docs and benchmarks change -> any final implementation slice should refresh source documentation before coding.

## Migration Plan

1. Add the architecture decision document.
2. Add OpenSpec requirements for decision gates.
3. Update README.
4. Validate docs/specs.
5. Archive this change.
