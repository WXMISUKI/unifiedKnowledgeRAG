# Production Indexing Architecture Decision

## Status

Draft for review. No production embedding model, vector database, queue worker, reranker, or graph store has been selected yet.

This document is a decision gate. Future implementation changes that add production indexing dependencies must reference this document and state which decisions have been approved.

## Context

The provider currently has stable local contracts for:

- source catalog and readiness
- document RAG retrieval contract
- local LlamaIndex retrieval with MockEmbedding
- explicit ingestion jobs
- durable local lifecycle store
- retry, cancellation, stale recovery, pagination, retention, and a local queued runner

That local runner is a contract and lifecycle proving ground. It is not production queue infrastructure.

Production indexing introduces decisions that affect cost, latency, recall, data residency, operations, and future GraphRAG support. These choices should be made together before code adds external dependencies.

## Decision Principles

- Keep MyPrivateAgent as the runtime control plane and this provider as the knowledge data plane.
- Keep HTTP contracts provider-neutral.
- Separate document RAG choices from GraphRAG storage choices.
- Prefer reversible adapters until a candidate is validated with project data.
- Require benchmark evidence before locking in retrieval infrastructure.
- Make data residency and operational ownership explicit.

## Decision 1: Embedding Model

### Candidates To Evaluate

- Hosted commercial embeddings, such as OpenAI, Voyage, Cohere, or cloud vendor embeddings.
- Local/open-source embeddings, such as BGE, E5, Jina, or Sentence Transformers families.
- Chinese/bilingual-focused embeddings if the primary corpus is Chinese or mixed Chinese-English.
- Multi-vector or sparse-capable models if hybrid retrieval becomes a requirement.

### Evaluation Criteria

- Chinese and bilingual retrieval quality.
- Domain vocabulary coverage.
- Cost per million tokens or documents.
- Latency under batch indexing and online query load.
- Deployment model: hosted API, private cloud, or fully local.
- Data residency and sensitive-data handling.
- Embedding dimensionality and vector database compatibility.
- Batch throughput and rate limits.
- Reranker compatibility.
- Versioning and reindex migration cost.

### Open Questions

- Is the first production corpus mostly Chinese, English, or mixed?
- Is external hosted embedding allowed for sensitive enterprise documents?
- Do we need offline/local inference as a hard requirement?
- What is the expected first corpus size and daily document churn?
- What accuracy target or benchmark set should decide the model?

## Decision 2: Vector Database

### Candidate Families

| Candidate | Strengths | Risks / Trade-offs | Good Fit |
| --- | --- | --- | --- |
| PostgreSQL + pgvector | Simple operations if PostgreSQL already exists; transactional metadata joins; exact and approximate search options such as HNSW/IVFFlat | Can become harder to tune at larger vector scale; hybrid retrieval usually needs extra text-search design | Small to medium corpus, strong relational metadata needs, low ops overhead |
| Qdrant | Dedicated vector database; strong filtering; dense/sparse/named vector and hybrid retrieval patterns in official docs | Extra service to operate; schema and payload design must be maintained | Provider-owned vector search with hybrid retrieval and moderate ops complexity |
| Milvus | Designed for larger-scale vector workloads; supports multi-vector and hybrid search patterns | More operational moving parts; may be heavier than early-stage needs | High volume, high throughput, dedicated vector infra team |
| Managed vector service | Lower infrastructure ownership; managed scaling and backups | Vendor lock-in, cost, data residency constraints | Teams prioritizing speed and managed operations |

### Evaluation Criteria

- Metadata filter expressiveness.
- Dense + sparse hybrid support.
- Index types and tuning knobs.
- Write/update/delete behavior.
- Backup and restore.
- Local development support.
- Deployment complexity on the target environment.
- Observability and operational tooling.
- Python ecosystem and LlamaIndex integration maturity.
- Reindex and schema migration story.

### Open Questions

- Do we already operate PostgreSQL in the target deployment?
- Is hybrid retrieval required in the first production slice?
- What are expected document count, chunk count, and query QPS?
- Who owns backup/restore and service monitoring?
- Are managed cloud services allowed?

## Decision 3: Queue And Worker Runtime

### Candidate Families

- Local explicit runner: current implementation; good for contract testing and development.
- Database-backed queue: simple if PostgreSQL is already selected.
- Redis/RQ/Celery-style worker: common Python worker ecosystem, extra service dependency.
- Message broker, such as RabbitMQ or Kafka: stronger decoupling, more operational overhead.
- Workflow engine, such as Temporal: durable orchestration, heavier adoption cost.

### Evaluation Criteria

- Lease and heartbeat semantics.
- Retry policy and poison-job handling.
- Cancellation and stale-running recovery.
- Worker concurrency and backpressure.
- Job observability and audit history.
- Deployment model and operations burden.
- Fit with MyPrivateAgent governance.

### Open Questions

- Is ingestion expected to run continuously or only by operator trigger?
- Is per-source concurrency needed?
- Do we need exactly-once semantics, or is idempotent at-least-once enough?
- What is the acceptable operational dependency footprint?

## Decision 4: Chunking, Hybrid Retrieval, And Reranking

### Candidate Choices

- Simple fixed-size chunks for early baseline.
- Structure-aware chunks for markdown, policy docs, manuals, or PDFs.
- Dense-only retrieval for semantic baseline.
- Dense + sparse hybrid retrieval for exact term and semantic recall.
- Reranker after vector/hybrid candidate generation.

### Evaluation Criteria

- Citation stability.
- Recall on domain benchmark questions.
- Precision in top-k evidence.
- Context length budget.
- Chunk overlap and duplication.
- Query latency.
- Reranker cost and deployment model.

### Open Questions

- Which document formats are production priority?
- Are citations required at section, paragraph, or document level?
- Do users ask exact policy/code terms that need sparse retrieval?
- What top-k evidence precision is acceptable before answer generation?

## Decision 5: GraphRAG Storage

GraphRAG is a separate architecture decision. It should not be hidden inside the document vector store.

### Candidate Families

- Neo4j / Neo4j GraphRAG for property graph, traversal, and graph-enhanced retrieval.
- PostgreSQL relational graph tables for simpler relation data.
- RDF/triplestore if ontology and semantic web standards are required.
- Specialized graph database if scale or traversal complexity demands it.

### Evaluation Criteria

- Entity and relation lifecycle.
- Ontology/versioning support.
- Multi-hop traversal.
- Full-text/vector hybrid support.
- Evidence traceability back to source documents or business records.
- Data import and reconciliation workflow.
- Operational ownership.

### Open Questions

- Is the first GraphRAG use case relationship-heavy enough to justify a graph database?
- Who owns ontology and entity resolution?
- Do graph answers need source document citations, business system citations, or both?

## Proposed Next Review

Before implementing production infrastructure, review these choices in order:

1. First production corpus and constraints.
2. Data residency and allowed external services.
3. Embedding candidate shortlist.
4. Vector database candidate shortlist.
5. Queue/worker operational model.
6. Chunking and retrieval benchmark plan.
7. GraphRAG storage priority and first graph use case.

## Current Recommendation

Do not add production embedding, vector database, queue, reranker, or graph store dependencies yet.

The safest next implementation slice is a benchmark harness that can run the same small corpus and query set across candidate embedding/retrieval adapters. That harness should be built only after we agree on the first candidate set.

## Benchmark Evidence Workflow

The initial benchmark harness lives in `app.services.retrieval_benchmark` and uses structured cases from `tests/fixtures/retrieval_benchmark_cases.json`.

Before approving production embedding, vector database, reranker, or hybrid retrieval implementation:

1. Add representative benchmark cases for the target corpus.
2. Include positive citation cases and expected empty-retrieval cases.
3. Run each candidate adapter through the same case set.
4. Compare hit rate, citation match rate, empty handling rate, category-level rates, and latency.
5. Export JSON and Markdown reports when comparing serious candidates.
6. Record the exported report paths in the relevant OpenSpec change before adding production dependencies.

The seed benchmark set currently covers policy, FAQ, evidence, paraphrase, multi-source, and empty retrieval categories. Before final production selection, expand those categories with real domain examples and review weak categories separately instead of relying only on a single aggregate score.

Preferred evidence format:

- JSON report for machine-readable comparison.
- Markdown report for human review in docs, PRs, or OpenSpec artifacts.
