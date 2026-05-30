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

## Source Document Fingerprint Diagnostics

Phase 2 document ingestion baseline evidence now includes lightweight source file drift diagnostics on `GET /api/rag/sources/{source_id}/documents`. Each local source document manifest can expose:

- source file presence
- current `sha256`
- expected provider-owned `sha256`
- byte size
- drift status: `in_sync`, `changed`, `missing`, or `unchecked`

This helps operators and external control planes see whether source files have changed before trusting citation anchors or deciding to reindex. It is intentionally read-only: it does not scan directories, parse complex document formats, create ingestion jobs, rebuild indexes, call embedding models, call Qdrant, or execute GraphRAG.

## Deployment Readiness Report

Phase 6 deployment and operations evidence is now represented by a local `deployment-readiness-v1` export. It consolidates:

- provider health
- provider preflight bindability
- provider contract smoke summary
- runtime configuration without secret values
- local embedding model artifact diagnostics
- operation notes for local/public-network/private-network review

The default local report can be regenerated with:

```powershell
conda run -n GRAPHRAG python scripts/export_deployment_readiness.py
```

The report is intentionally read-only. It does not start ingestion jobs, rebuild indexes, download models, call embedding services, call Qdrant, or execute graph queries. External control planes still own registration, heartbeat governance, audit policy, and source-to-agent binding decisions.

## Reindex Readiness Plan

Phase 6 backup and reindex evidence is now also represented by a local `reindex-readiness-v1` export. It consolidates:

- configured source catalog entries
- source file presence under `RAG_SOURCE_DIR`
- persisted source index status
- latest logical ingestion job metadata
- lifecycle job status counts
- per-source recommended operator action

The default local report can be regenerated with:

```powershell
conda run -n GRAPHRAG python scripts/export_reindex_readiness.py
```

The report is intentionally read-only. It does not create ingestion jobs, rebuild indexes, compact job history, download embedding models, call Qdrant, or execute GraphRAG. It is a review artifact for local/public-network/private-network deployment planning before an operator chooses whether to back up indexes or run explicit ingestion.

Reindex readiness now consumes source document fingerprint diagnostics. A source with `drift_status=changed` is reported as needing `run_ingestion_job`; a source with `drift_status=unchecked` asks for `review_source_fingerprint`. This connects Phase 2 source freshness evidence to Phase 6 operations planning while still leaving actual ingestion and reindex execution explicit.

## Provider Handoff Bundle

Phase 6 integration and operations evidence is now consolidated by a local `provider-handoff-bundle-v1` export. It gives MyPrivateAgent or a deployment reviewer one review entry point over:

- provider identity and contract version
- provider integration probe evidence
- provider contract smoke evidence
- deployment readiness evidence
- reindex readiness evidence
- per-artifact presence, status, summary, and recommended action

The default local bundle can be regenerated with:

```powershell
conda run -n GRAPHRAG python scripts/export_provider_handoff_bundle.py
```

The bundle is intentionally read-only. It does not regenerate prerequisite reports, call provider HTTP endpoints, execute retrieval or answer composition, start ingestion jobs, rebuild indexes, download models, call Qdrant, or execute GraphRAG. External control planes still own provider registration, heartbeat governance, audit policy, source-to-agent binding, and final answer policy.

## Provider Handoff Evidence Refresh

Phase 6 evidence freshness is now represented by a local `provider-handoff-refresh-v1` export. It regenerates the handoff prerequisites in order, then regenerates the handoff bundle:

1. provider integration probe
2. provider contract smoke
3. deployment readiness
4. reindex readiness
5. provider handoff bundle

The default local refresh can be run with:

```powershell
conda run -n GRAPHRAG python scripts/export_provider_handoff_refresh.py
```

The refresh summary is written under `docs/integration/provider-handoff-refresh/`. It is intentionally local and bounded to evidence files. It does not start a server, add HTTP endpoints, create ingestion jobs, explicitly rebuild indexes, download models, call Qdrant, or execute GraphRAG. It is the preferred command before handing the provider evidence package to MyPrivateAgent or a deployment reviewer.

## Provider Handoff API

Phase 6 handoff evidence is also exposed through a lightweight read-only HTTP discovery endpoint:

```text
GET /api/provider/handoff
```

The endpoint returns the current `provider-handoff-bundle-v1` summary over existing local evidence artifacts. It does not regenerate prerequisite reports, start ingestion jobs, rebuild indexes, execute retrieval or answer composition, download models, call Qdrant, or execute GraphRAG.

This gives MyPrivateAgent and other external control planes an API-native way to inspect the handoff bundle while preserving the provider boundary. Registration, heartbeat governance, audit policy, source-to-agent binding, and final answer policy remain caller-owned.

## Enterprise Document Ingestion Boundary

Phase 2 now includes a read-only source ingestion preflight endpoint:

```text
GET /api/ingestion/sources/{source_id}/preflight
```

The endpoint reports file presence, document format support, lightweight parser status, chunk count, chunk preview, citation anchor readiness, current index lifecycle status, and recommended action before an operator creates an ingestion job.

This boundary is intentionally lightweight. Markdown is the only supported parser in this slice. PDF, Word, Excel, HTML, scanned images, and unknown formats are reported as unsupported rather than parsed. The endpoint does not create ingestion jobs, write lifecycle records, rebuild indexes, call embedding models, call Qdrant, execute retrieval or answer composition, or execute GraphRAG.

The next parser-related work should be driven by real corpus demand and separate evidence-backed OpenSpec changes, not by adding every document parser dependency up front.

## Provider API Access Guard

Phase 6 deployment work now includes a default-off provider API key guard. When `PROVIDER_API_KEY` is configured, `/api/*` requests require either:

```text
Authorization: Bearer <token>
X-Provider-Api-Key: <token>
```

`GET /health` remains public for deployment health checks.

This is a lightweight component access guard, not an identity or policy system. MyPrivateAgent or another external control plane still owns user identity, roles, approvals, audit policy, source-to-agent binding, and final answer policy.
