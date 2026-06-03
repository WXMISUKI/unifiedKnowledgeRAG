# Open-Source RAG Engine Evaluation Roadmap

## Purpose

This roadmap records the selection strategy for mature open-source RAG engines without turning `unifiedKnowledgeRAG` into a heavy platform.

The recommended direction is to keep this project as a stable, lightweight, auditable knowledge provider contract layer. Mature engines can be reused behind the provider boundary when evidence proves they are better for a specific job. MyPrivateAgent and other callers should keep integrating through the provider contract rather than binding directly to a single RAG framework.

## Current Decision

Verdict: `continue_provider_first_with_candidate_backends`.

The project should not be replaced by a full platform at this stage. The short-term goal is smooth local RAG consumption by MyPrivateAgent. The medium-term goal is evidence-backed candidate backend comparison. The long-term goal is an engine-agnostic provider whose public contract remains stable while the underlying retrieval engine can change.

## Strategic Timeline

| Horizon | Goal | Primary Work | Exit Criteria | Non-Goals |
| --- | --- | --- | --- | --- |
| Short term | MyPrivateAgent local RAG works predictably | Keep LlamaIndex baseline; keep evidence pack and local integration smokes current; use Qdrant/BGE-M3/hybrid/pgvector only through gates | MyPrivateAgent can discover, preflight, retrieve, consume citations, and review source-binding evidence locally | Replace provider with RAGFlow/Dify/Langflow; promote candidate runtime defaults |
| Medium term | Compare reusable engines fairly | Spike Haystack, RAGFlow, LightRAG, pgvector, and continued Qdrant+BGE-M3 as optional backend candidates | Each candidate has comparable quality, citation, FP/FN, latency, deployment, and operations evidence | Treat GitHub popularity as production approval |
| Long term | Stable contract, replaceable engines | Define backend adapter boundary; keep framework-specific response shapes internal; promote only after customer-like evidence and operations sign-off | Runtime backend choice is explicit, reversible, and invisible to callers | Move caller control plane or final answer policy into this provider |

## Short-Term Direction: MyPrivateAgent Local RAG

The next practical objective is not broader engine migration. It is to make MyPrivateAgent's local RAG path boring and dependable.

Required short-term posture:

- Keep the existing provider HTTP contract stable.
- Keep `evidence_pack-v1` as the caller-facing answer support shape.
- Keep mock/fixture retrieval as a deterministic local baseline.
- Keep LlamaIndex as the current implementation baseline unless a separate gate says otherwise.
- Keep local `PROVIDER_API_KEY` assumptions simple and explicit for local testing.
- Keep GraphRAG discovery as planned-boundary evidence, not execution.
- Keep Qdrant, BGE-M3, hybrid retrieval, aggregation, and relation-aware grading as candidate/review evidence until all promotion gates close.
- Keep the Phase 12e local pgvector probe environment optional and explicit until the live probe can be rerun locally.

Recommended next short-term task families:

1. MyPrivateAgent local integration hardening: confirm provider discovery, retrieve consumption, handoff, source-binding preview, and access-key posture against the local recommended URL.
2. Retrieval contract stability: keep citation-bearing retrieve responses and fail-closed insufficient-evidence behavior stable.
3. Candidate backend evaluation preparation: define a common candidate adapter/evidence shape before adding new backend spikes.

For local hardening handoff, this means one concrete execution order:

- first make local RAG integration evidence deterministic at `http://127.0.0.1:8020`,
- then generate/read the hardening profile and smoke for manifest/contract/handoff/source-binding/retrieval readiness,
- keep source binding and runtime default boundaries unchanged until candidate promotion gates are closed.

## Medium-Term Direction: Candidate Backend Spikes

Medium-term work should compare mature engines under this project's own constraints rather than adopting their full product surface.

| Candidate | Why Evaluate | Expected Use | Gate Before Promotion |
| --- | --- | --- | --- |
| LlamaIndex | Already aligned with current RAG baseline and common RAG concepts such as loading, indexing, storing, querying, and evaluation | Baseline implementation and adapter reference | Continue unless replacement has stronger evidence |
| Qdrant | Dedicated vector database with snapshot/restore operations path | Vector-store candidate for larger local/private deployments | Retrieval quality, latency, backup/restore, reindex, private-network evidence |
| pgvector | Vector search inside PostgreSQL with operational reuse | Candidate when Postgres consolidation is preferred | Quality/latency parity, schema isolation, backup/recovery, DBA ownership |
| BGE-M3 | Local Chinese-heavy embedding candidate | Local/private embedding path | Artifact checksum, quality/latency comparison, deployment footprint |
| Haystack | Modular RAG pipeline and components | Optional backend spike for pipeline composition | Citation fidelity, adapter complexity, dependency footprint |
| RAGFlow | Mature RAG product with deep document parsing and grounded citation features | Product reference or external backend spike | Heavy dependency review, control-plane boundary, parser need from real corpus |
| LightRAG | Lightweight graph-aware RAG candidate | Relation-heavy retrieval spike | Entity/relation/path cases and GraphRAG boundary review |
| Microsoft GraphRAG | Graph indexing architecture reference | Graph evidence design reference | Concrete relationship-heavy use case and cost/time benchmark |
| Dify | LLM app platform with workflow/RAG/agent capabilities | External integration or product reference | Do not absorb platform control plane |
| Langflow | Visual workflow and agent/RAG platform | External integration or product reference | Do not absorb platform control plane |

## Long-Term Direction: Engine-Agnostic Provider

The long-term architecture should make engine changes possible without caller rewrites.

Target shape:

- A small provider-owned backend adapter boundary behind current APIs.
- A common candidate evidence schema for quality and operations comparison.
- Stable caller-facing evidence envelopes, citation policy, source metadata, and readiness diagnostics.
- Explicit runtime selection and rollback mechanics only after promotion approval.
- GraphRAG execution only after relationship-heavy use cases justify it.

## Evaluation Gates

Every engine candidate should be reviewed against the same gate families:

- MyPrivateAgent local contract compatibility.
- Citation fidelity and citation granularity.
- Customer-like Chinese benchmark coverage.
- False-positive and false-negative review.
- Exact-term, alias, OCR-noise, split-chunk, and unsupported-domain behavior.
- Latency and resource profile.
- Local, private-network, and future online deployment feasibility.
- Data residency and offline/private-network readiness.
- Backup, restore, reindex, and rollback posture.
- Dependency, license, maintenance, and upgrade risk.
- GraphRAG boundary impact.

Promotion states:

- `keep_current_default`: evidence does not justify promotion.
- `continue_spike`: evidence is promising but gates remain open.
- `eligible_for_promotion_review`: evidence is strong enough for a separate runtime promotion change.
- `reference_only`: useful product/architecture reference, but not a provider backend candidate.

## External Sources Reviewed

- LlamaIndex RAG documentation: https://developers.llamaindex.ai/python/framework/understanding/rag/
- Haystack documentation: https://docs.haystack.deepset.ai/docs/intro
- Qdrant snapshots documentation: https://qdrant.tech/documentation/tutorials/create-snapshot/
- pgvector repository: https://github.com/pgvector/pgvector
- RAGFlow repository: https://github.com/infiniflow/ragflow
- LightRAG repository: https://github.com/HKUDS/LightRAG
- Microsoft GraphRAG indexing pipeline documentation: https://microsoft-graphrag.mintlify.app/concepts/indexing-pipeline
- Dify repository: https://github.com/langgenius/dify
- Langflow repository: https://github.com/langflow-ai/langflow

## Boundary Statement

This roadmap does not approve runtime migration. It does not promote Qdrant, BGE-M3, hybrid retrieval, pgvector, GraphRAG, rerankers, answer composition, or heavy document parsers to defaults.

The provider remains responsible for evidence, citations, readiness metadata, diagnostics, and integration evidence. MyPrivateAgent or another caller remains responsible for final answer policy, orchestration, registration, heartbeat governance, audit, approvals, source-to-agent binding, and user-facing workflows.
