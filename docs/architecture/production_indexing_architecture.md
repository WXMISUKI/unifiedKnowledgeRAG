# Production Indexing Architecture Decision

## Status

Draft for review. Qdrant is the primary vector-store candidate for evaluation, but no production embedding model, queue worker, reranker, or graph store has been selected yet.

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
| Qdrant | Dedicated vector database; strong filtering; dense/sparse/named vector and hybrid retrieval patterns in official docs | Extra service to operate; schema and payload design must be maintained | Primary candidate for provider-owned vector search, Chinese-heavy enterprise RAG, and future hybrid retrieval |
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

Do not add production embedding, queue, reranker, or graph store dependencies yet. Qdrant is approved only as an evaluation candidate adapter until live benchmark evidence exists.

The safest next implementation slice after the candidate adapter is live Qdrant ingestion/retrieval behind explicit configuration, paired with an undecided embedding adapter so public-network local testing and future private-network deployment can share the same provider contract.

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

The current Chinese-heavy seed set has been expanded beyond exact-match policy lookup. It includes exception policy, operational escalation, SLA/timeliness, multi-intent, cross-source, paraphrase, evidence, and business-like empty cases. This gives hosted/local embedding candidates a more realistic first comparison surface while still remaining small enough for deterministic local tests.

Passing this seed set is not final production acceptance. Before production promotion, add customer-specific documents and queries, then compare category-level misses instead of relying only on aggregate hit rate.

Preferred evidence format:

- JSON report for machine-readable comparison.
- Markdown report for human review in docs, PRs, or OpenSpec artifacts.

## Candidate Evaluation Workflow

Candidate evaluation lives in `app.services.retrieval_benchmark` and intentionally remains service-only. It lets each candidate carry a stable id, backend, description, and optional metadata such as embedding model, vector store, reranker, or notes.

Use this workflow before proposing production retrieval infrastructure:

1. Define the candidate shortlist with explicit metadata.
2. Run `evaluate_retrieval_candidates(...)` against the same benchmark cases.
3. Export per-candidate JSON and Markdown evidence with stable candidate-based filenames.
4. Reference those files from the OpenSpec change that proposes the production dependency.

Current candidate evaluation only maps candidates to existing local backends. Adding a new production candidate adapter remains a separate decision and should happen only after we agree on the embedding, vector store, reranker, or hybrid retrieval option being evaluated.

## Qdrant Evaluation Path

Qdrant is the first vector-store candidate because it gives this provider a dedicated vector search layer without requiring existing PostgreSQL or Neo4j operations.

Local/public-network path:

1. Run Qdrant locally, usually with Docker.
2. Use a hosted embedding model only for developer evaluation.
3. Keep payload metadata compatible with future private-network deployment.
4. Export candidate benchmark reports before promoting the adapter.

Private-network enterprise path:

1. Run Qdrant inside the target network.
2. Replace hosted embeddings with a local Chinese/bilingual embedding service.
3. Add a local reranker only after retrieval benchmark evidence shows the need.
4. Keep GraphRAG storage separate, likely behind a later Neo4j experiment.

Current Qdrant implementation status:

- Qdrant settings are available.
- Qdrant evidence point and payload mapping are available.
- Source/tenant/document/ACL filter mapping is available.
- Live Qdrant collection preparation, chunk upsert, and vector query helpers are available.
- Query text embedding and reranking are intentionally deferred.
- Qdrant is not the default retrieval backend.

## Qdrant Live Adapter Boundary

The live Qdrant adapter accepts vectors, not text. This is deliberate:

- vector-store behavior can be tested independently from embedding quality
- public-network hosted embeddings and private-network local embeddings can share the same Qdrant contract
- benchmark evidence can isolate vector-store behavior from model-selection behavior

Before promoting Qdrant beyond candidate status, the next evidence steps are:

1. Add an embedding adapter interface.
2. Evaluate at least one hosted and one local Chinese/bilingual embedding candidate.
3. Run the same retrieval benchmark cases through Qdrant.
4. Decide whether reranking is required from benchmark misses, not by assumption.

## Embedding Adapter Boundary

Embedding is now a provider-neutral adapter boundary. The default `mock` adapter is deterministic and local, but it is not a semantic retrieval model.

Hosted and local providers are intentionally present only as fail-closed placeholders until explicit model decisions are approved:

- hosted candidates are useful for local/public-network experiments
- local candidates are required for private-network enterprise deployments
- both paths must produce the same vector contract for Qdrant

Before approving a real embedding provider:

1. Define candidate metadata, including language coverage, vector size, deployment model, and data residency.
2. Run candidate benchmark reports against Chinese-heavy cases.
3. Confirm Qdrant collection vector size and reindex migration plan.
4. Decide whether reranking is required based on benchmark misses.

## Chinese Embedding Candidate Evaluation

Embedding model selection is now represented as local candidate evidence before any provider is approved. The evaluation catalog currently includes:

| Candidate | Provider Family | Intended Path | Notes |
| --- | --- | --- | --- |
| `mock-hash-v1` | mock | local contract baseline | deterministic only; not semantic retrieval |
| `qwen-embedding-candidate` | hosted | public-network Chinese-heavy experiment | data egress and private deployment must be reviewed |
| `bge-m3-local-candidate` | local | private-network Chinese-heavy experiment | runtime footprint and serving stack must be benchmarked |
| `openai-embedding-candidate` | hosted | public hosted multilingual baseline | useful for comparison only if public egress is approved |

The service-level helper `evaluate_embedding_candidates(...)` exports JSON and Markdown evidence with candidate metadata, readiness notes, and enterprise criteria coverage. It does not call real embedding services.

Before implementing a real embedding adapter, we should use this evidence shape to decide:

1. Which hosted candidate is acceptable for public-network local testing.
2. Which local candidate is viable for private-network enterprise deployment.
3. What vector dimension Qdrant collections should use.
4. Whether candidate misses indicate a reranker or hybrid retrieval requirement.

## Qdrant Text Query Orchestration

Qdrant text query orchestration now connects query text to the embedding adapter and Qdrant vector query path. This makes the adapter executable, but it is not production promotion.

Remaining gaps before production use:

1. Ingest real source documents into Qdrant with a real embedding candidate.
2. Run benchmark reports against Chinese-heavy cases.
3. Compare hosted and local embedding candidates under the same Qdrant payload contract.
4. Decide whether dense-only retrieval is enough or whether sparse/hybrid retrieval is needed.
5. Add reranker only if benchmark misses justify it.

Until those evidence steps are complete, Qdrant stays opt-in and the default retrieval backend remains unchanged.

## Qdrant Source Ingestion Baseline

Qdrant source ingestion can now read local markdown source files, create paragraph-level evidence chunks, embed them through the configured adapter, upsert them to Qdrant, and mark source index lifecycle status ready.

This is a baseline ingestion path, not the final enterprise document processing strategy.

Current baseline:

- source format: markdown
- chunking strategy: `markdown-paragraph-v1`
- embedding: configurable adapter, default mock
- vector store: explicit Qdrant backend
- lifecycle: existing ingestion jobs and source status manifest

Remaining enterprise decisions:

1. PDF, Word, table, and scanned document parsing.
2. Token-aware chunk sizing and overlap for Chinese-heavy documents.
3. Section-level and document-level summary chunks.
4. Incremental reindexing by content hash.
5. Deletion/update semantics for retired source versions.
6. Benchmark-driven comparison of chunking strategies.
