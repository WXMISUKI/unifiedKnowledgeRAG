# Lightweight Provider Roadmap

## Purpose

`unifiedKnowledgeRAG` is a lightweight external knowledge provider for MyPrivateAgent and other callers. Its job is to return trustworthy evidence, citations, readiness metadata, and integration evidence. It is not the agent runtime, policy engine, approval system, memory system, or final response renderer.

The roadmap exists to keep future work orderly without making the project heavy. Each phase defines the smallest useful outcome and the evidence needed before runtime defaults change.

## Responsibility Boundary

| Area | This Provider Owns | Caller Owns |
| --- | --- | --- |
| Identity and policy | Provider id, contract version, capability ids | Agent identity, roles, policies, approvals |
| Retrieval | Evidence documents, snippets, scores, citations, traces | When to retrieve and how to use retrieved evidence |
| Answer support | Evidence packaging, optional cited-answer diagnostics, validation metadata | Final user-facing answer, tone, workflow, refusal policy |
| Knowledge lifecycle | Source catalog, ingestion jobs, index readiness, retrieval backend metadata | Business decision to bind sources to agents |
| GraphRAG | Schema boundary and future graph evidence contracts | Deciding whether a task needs graph capability |
| Operations | Provider health, preflight, smoke, integration probe evidence | Registration, heartbeat governance, audit policy |

## Lightweight Principles

- Prefer stable contracts and evidence over broad framework adoption.
- Keep candidate work reversible until evidence justifies promotion.
- Do not add production infrastructure just because a mature project has it.
- Do not move MyPrivateAgent control-plane responsibilities into this module.
- Keep document RAG, hybrid retrieval, reranking, LLM answer composition, and GraphRAG as separate gates.
- Treat benchmark and smoke evidence as review inputs, not as automatic production approval.

## Phases

| Phase | Goal | Completion Evidence | Non-Goals |
| --- | --- | --- | --- |
| 0. Provider Contract Baseline | External callers can discover, preflight, and bind the provider | Health, manifest, preflight, capabilities, contract smoke, integration probe evidence | Production vector/graph infrastructure |
| 1. Lightweight Roadmap Gates | Future work has a clear phase and promotion criteria | This roadmap plus `provider-roadmap` OpenSpec requirements | Building features only to satisfy a roadmap |
| 2. Enterprise Document Ingestion Baseline | Documents can be loaded, chunked, indexed, and diagnosed with stable metadata | Source lifecycle, chunking candidate evidence, index readiness, citation stability | Complex OCR/table parsing before real corpus demand |
| 3. Retrieval Quality Promotion | Runtime retrieval defaults are chosen by evidence | Chinese/customer benchmark reports, exact-term and empty-stress evidence, threshold/hybrid/rerank gates | Promoting hybrid/reranker from a single positive metric |
| 4. Evidence Packaging For Caller Answers | Callers receive enough context to answer without hallucination | Evidence pack, citations, trace, validation metadata, insufficient-evidence behavior | Provider taking over caller persona or final answer policy |
| 5. Use-Case-Driven GraphRAG | Graph execution exists only after relationship-heavy use cases are real | Graph schema, entity/relation/path benchmark, source evidence rules, graph-store decision | Adding Neo4j or ontology workflow as a default dependency |
| 6. Deployment And Operations | Provider can run as a component in local/public/private-network paths | Readiness reports, model artifact guidance, backup/reindex notes, integration evidence | Becoming a general platform control plane |

## Phase Gate Rules

Every future OpenSpec change should state which phase it advances. If it does not fit a phase, the proposal should explain why.

Runtime promotion requires evidence:

- Embedding model promotion needs benchmark evidence and deployment/data-residency review.
- Vector-store promotion needs ingestion, retrieval, filtering, and reindex evidence.
- Hybrid retrieval promotion needs both recall improvement and false-positive control.
- Reranker promotion needs top-k quality evidence and latency/cost review.
- Answer composer promotion needs citation validation and fail-closed behavior.
- GraphRAG promotion needs concrete graph use cases, graph evidence rules, and operational ownership.

Candidate changes may add adapters, fixtures, reports, or local evaluation helpers, but they should not change runtime defaults unless the relevant gate is explicitly satisfied.

## Near-Term Direction

The current provider already has Phase 0 mostly complete. The most valuable next work should stay lightweight:

1. Keep the binding/integration evidence current.
2. Use the roadmap to choose the next small phase-aligned OpenSpec change.
3. Prefer document ingestion and evidence packaging improvements before GraphRAG execution.
4. Promote Qdrant/BGE-M3/hybrid behavior only after customer-like benchmark evidence supports it.
5. Keep GraphRAG as a later, use-case-driven phase rather than a default dependency.

## Retrieval Evidence Pack

Phase 4 evidence packaging is now represented by `evidence_pack-v1` metadata on successful RAG retrieve and answer envelopes. The pack is retrieval-owned and deterministic; it gives callers a stable bundle with:

- pack id and version
- status: `answerable` or `insufficient_evidence`
- reason: `documents_returned` or `no_documents`
- citation policy: `use_only_returned_citations`
- allowed citations aligned to returned documents
- evidence count and score summary
- requested source ids, retrieval backend, filter context, and compact evidence entries

This does not make the provider the final answer policy owner. MyPrivateAgent or another caller still owns user-facing response style, refusal policy, approval workflow, and final orchestration. The provider only exposes trustworthy evidence and diagnostics so callers can avoid hallucinating beyond returned citations.
