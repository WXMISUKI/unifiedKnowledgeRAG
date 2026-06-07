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

## Phase 3 Gap Matrix

Phase 3 promotion review is now easier to read as a single local gap matrix:

`docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-gap-matrix.md`

The matrix is a lightweight review artifact. It consolidates current evidence for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, multi-chunk aggregation, relation-aware grading, and deployed smoke so reviewers can see the open promotion gaps without changing runtime defaults.

## Phase 3 Readiness Export

The same promotion picture is also exported as machine-readable evidence:

`docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.json`

`docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.md`

The readiness export is read-only and local. Provider handoff and handoff refresh can surface it as optional review evidence so reviewers do not have to stitch the gap matrix together by hand.

## Phase 3 Candidate Evaluation Protocol

Phase 3 now also has a local candidate evaluation protocol that standardizes promotion-review expectations across candidate gate families:

`docs/benchmark/chinese-seed/retrieval-candidate-evaluation-protocol/phase3-retrieval-candidate-evaluation-protocol.md`

The protocol is intentionally read-only and evaluation-only. It defines required evidence classes for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, relation-aware grading, and deployed smoke follow-up, while preserving `keep_runtime_defaults` until separate promotion gates are explicitly closed.

## Phase 3 Candidate Runtime Diagnostics

Phase 3 now also has a machine-readable runtime diagnostics export for candidate promotion prerequisites:

`docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json`

`docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.md`

The export is read-only and local. It summarizes runtime-adjacent prerequisite checks such as retrieval backend mode, embedding provider and artifact status, readiness export status, and deployed smoke evidence presence, while preserving `keep_runtime_defaults`.

## Phase 3 Hybrid Cross-Case FP/FN Smoke

Phase 3 now also has a compact cross-case smoke artifact for hybrid-risk visibility:

`docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json`

`docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.md`

The smoke is read-only and local. It verifies that key risk-case coverage, false-positive trap alignment, and positive-control outcomes remain visible in existing baseline and FP/FN evidence without changing runtime defaults.

## Phase 3 Hybrid Runtime Promotion Decision Readiness

Phase 3 now also has a machine-readable final promotion-review readiness export that consolidates Phase 3 and Phase 6 bridge evidence:

`docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.json`

`docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.md`

The export is read-only and local. It summarizes required evidence-chain signals and open gates for the hybrid runtime promotion decision while preserving `keep_runtime_defaults` until all required gates are explicitly closed.

## Phase 3 Hybrid Runtime Promotion Decision Smoke

Phase 3 now also has a compact smoke artifact for final promotion-review evidence-chain completeness:

`docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.json`

`docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.md`

The smoke is read-only and local. It validates contract/readiness linkage and prerequisite evidence-chain presence without changing runtime defaults or promotion decisions.

## Phase 3 Hybrid Runtime Promotion Decision Record

Phase 3 now also has a final decision record for the current hybrid runtime promotion cycle:

`docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-record.md`

The record is documentation-only. It captures the current verdict and open gates for promotion while preserving the boundary that runtime defaults remain unchanged until a separate approved promotion change.

## Graph Boundary Preflight

Phase 5 graph work remains use-case driven, but provider preflight now summarizes the graph boundary that already exists: graph schema count, graph ids, graph statuses, and graph store labels. This lets MyPrivateAgent or another control plane discover that graph namespaces are present while still seeing `execution_status=planned`.

This does not implement GraphRAG execution. It does not connect to Neo4j, extract entities, build ontology workflows, create graph indexes, execute graph queries, or change runtime retrieval behavior. Graph execution still requires a separate relationship-heavy use case, source evidence rules, benchmark evidence, and operational ownership.

Provider contract smoke also validates `GET /api/graph/schemas` as graph boundary evidence. It records graph ids, graph count, graph status, graph store labels, and entity/relation type counts while preserving `POST /api/graph/query` as a planned not-implemented boundary.

## Phase 5 Graph Use-Case Readiness Contract

Phase 5 now also has a local graph use-case readiness contract that says which questions are graph-worthy and which should stay in document RAG:

`docs/benchmark/chinese-seed/graph-use-case-readiness/phase5-graph-use-case-readiness-contract.md`

The contract is intentionally read-only and review-oriented. It names concrete relationship-heavy cases, keeps single-source citation lookups in document RAG, and leaves GraphRAG execution, graph storage, and ontology workflows behind separate evidence-backed changes.

## Phase 5 Graph Use-Case Readiness Export

Phase 5 now also has a machine-readable readiness export that consolidates the graph use-case contract, provider preflight graph boundary, and provider contract smoke evidence into a local review artifact:

`docs/benchmark/chinese-seed/graph-use-case-readiness/phase5-graph-use-case-readiness.json`

`docs/benchmark/chinese-seed/graph-use-case-readiness/phase5-graph-use-case-readiness.md`

The export is intentionally read-only. It lets reviewers and handoff consumers inspect the current GraphRAG boundary without changing runtime defaults, adding graph execution, or introducing graph-store dependencies.

## Phase 5 Graph Boundary Smoke Summary

Phase 5 now also has a compact graph boundary smoke summary that condenses the graph schema discovery and planned graph query checks from provider contract smoke into a local review artifact:

`docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.json`

`docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.md`

The summary is intentionally read-only. It gives reviewers a small graph-boundary-only smoke artifact without changing runtime defaults or adding GraphRAG execution.

## Retrieval Evidence Pack

Phase 4 evidence packaging is now represented by `evidence_pack-v1` metadata on successful RAG retrieve and answer envelopes. The pack is retrieval-owned and deterministic; it gives callers a stable bundle with:

- pack id and version
- status: `answerable` or `insufficient_evidence`
- reason: `documents_returned` or `no_documents`
- citation policy: `use_only_returned_citations`
- allowed citations aligned to returned documents
- evidence count and score summary
- requested source ids, retrieval backend, filter context, and compact evidence entries
- provider-owned provenance on each evidence entry when available:
  `source_path`, `chunk_id`, `chunking_strategy`, and `citation_anchor`

This provenance is intentionally attached to `metadata.evidence_pack.evidence[]` instead of the top-level returned `documents` list, so caller integrations keep a compact document envelope while still receiving enough traceability for grounding and retrieval debugging.

This does not make the provider the final answer policy owner. MyPrivateAgent or another caller still owns user-facing response style, refusal policy, approval workflow, and final orchestration. The provider only exposes trustworthy evidence and diagnostics so callers can avoid hallucinating beyond returned citations.

## Phase 4 Consumption Contract

Phase 4 now also has a read-only caller consumption contract that explains how to use the existing evidence pack fields safely:

`docs/benchmark/chinese-seed/evidence-pack-consumption-contract/phase4-evidence-pack-consumption-contract.md`

The contract is intentionally local and review-oriented. It translates the existing `answerable` and `insufficient_evidence` evidence pack semantics into caller-facing rules without changing runtime behavior or final answer ownership.

## Phase 4 Readiness Export

Phase 4 now also has a machine-readable readiness export that consolidates the consumption contract, provider contract smoke, and supporting evidence into a local review artifact:

`docs/benchmark/chinese-seed/evidence-pack-readiness/phase4-evidence-pack-readiness.md`

The export is intentionally read-only. It helps reviewers and handoff consumers inspect current evidence-pack readiness without changing runtime defaults, caller ownership, or provider HTTP contracts.

## Phase 4 Caller Consumption Smoke

Phase 4 now also has a caller-consumption smoke that directly exercises `build_evidence_pack` for the answerable and insufficient-evidence branches:

`docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.md`

The smoke is intentionally local and read-only. It confirms the caller-facing allowlist and fail-closed behavior without duplicating provider HTTP flow or changing runtime defaults.

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

## Liveness And Readiness Probes

Phase 6 high-availability deployment work now separates process liveness from traffic readiness:

```text
GET /live
GET /ready
GET /health
```

`/live` is a side-effect-free process probe and does not construct retrieval backends, inspect index lifecycle, run answer readiness, call embedding/vector stores, create ingestion jobs, or execute GraphRAG. `/ready` returns the provider readiness contract used to decide whether the instance should receive traffic: HTTP 200 when `status=ok`, and HTTP 503 when `status=degraded` while preserving the same diagnostic body. `/health` remains compatible with existing callers and returns HTTP 200 with the readiness body. This is intentionally lightweight; orchestration, alert routing, autoscaling policy, heartbeat governance, registration, and audit policy remain outside this provider.

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

Phase 2 source onboarding now also includes source package and chunk manifest diagnostics on the existing source document and ingestion preflight surfaces. `source_package` records lightweight business and parsing expectations such as domain, language, sensitivity, supported formats, default chunking strategy, citation granularity, and allowed parser statuses. `chunk_manifest` records deterministic markdown chunk ids, citations, chunking strategy, source path, character count, and capped preview text. These fields help operators review enterprise source readiness before ingestion while keeping parser expansion, indexing, embedding, vector-store promotion, and GraphRAG behind separate gates.

## Phase 2 Source-Format Demand Readiness

Phase 2 now also has a machine-readable source-format demand readiness export:

`docs/operations/source-format-demand/phase2-source-format-demand-readiness.json`

`docs/operations/source-format-demand/phase2-source-format-demand-readiness.md`

The export is read-only and local. It summarizes markdown baseline posture, unsupported/non-markdown demand signals, and open expansion gates from current source-binding evidence without enabling non-Markdown parser runtime behavior.

## Phase 2 Unsupported-Format Negative-Control Smoke

Phase 2 now also has a compact unsupported-format negative-control smoke report:

`docs/smoke/source-format-demand/phase2-unsupported-format-negative-control-smoke.json`

`docs/smoke/source-format-demand/phase2-unsupported-format-negative-control-smoke.md`

The smoke is read-only and local. It keeps markdown positive controls and unsupported/non-markdown negative controls visible in one artifact, without changing ingestion execution or parser defaults.

## Phase 2 Parser Expansion Decision Record

Phase 2 now also has a parser-expansion decision record for the current cycle:

`docs/operations/source-format-demand/phase2-parser-expansion-decision-record.md`

The record is documentation-only governance evidence. It captures the current `keep_markdown_baseline` verdict, evidence basis, and open gates while preserving parser expansion as a separate future change.

## Phase 7 Provider Handoff Acceptance Contract

Cross-phase handoff acceptance is now documented as a local contract:

`docs/operations/provider-release-readiness/phase7-provider-handoff-acceptance-contract.md`

The contract is read-only and reviewer-facing. It defines required handoff evidence, optional review evidence, and status semantics (`ready/review/blocked`) without changing runtime defaults. It also preserves the boundary that local handoff acceptance does not imply runtime default promotion.

## Phase 7 Provider Release Readiness

Phase 7 now also has a machine-readable cross-phase provider release-readiness export:

`docs/operations/provider-release-readiness/phase7-provider-release-readiness.json`

`docs/operations/provider-release-readiness/phase7-provider-release-readiness.md`

The export is read-only and local. It summarizes required handoff gates and representative Phase 2-6 review signals, and it separates `ready_for_local_provider_handoff` from `ready_for_runtime_default_promotion`.

## Phase 7 Cross-Phase Handoff Consistency Smoke

Phase 7 now also has a compact cross-phase handoff consistency smoke artifact:

`docs/smoke/cross-phase-handoff/phase7-cross-phase-handoff-consistency-smoke.json`

`docs/smoke/cross-phase-handoff/phase7-cross-phase-handoff-consistency-smoke.md`

The smoke is read-only and local. It checks that key phase decisions and smoke/readiness outputs remain aligned with the current Phase 7 release-readiness decision.

## Phase 7 Provider Release Decision Record

Phase 7 now also has a release decision record for the current cycle:

`docs/operations/provider-release-readiness/phase7-provider-release-decision-record.md`

The record is documentation-only governance evidence. It captures the current verdict that local handoff is ready while runtime default promotion remains gated.

## Phase 8 Live URL Validation Execution Contract

Phase 8 now introduces a live URL validation execution contract:

`docs/operations/live-url-validation/phase8-live-url-validation-execution-contract.md`

The contract is execution-oriented and read-only. It defines required live-validation inputs, allowed endpoint scope, and status semantics while preserving the boundary that live URL validation evidence does not imply runtime default promotion.

## Phase 8 Live URL Validation Readiness

Phase 8 now also has a machine-readable live URL validation readiness export:

`docs/operations/live-url-validation/phase8-live-url-validation-readiness.json`

`docs/operations/live-url-validation/phase8-live-url-validation-readiness.md`

The export is read-only and local. It summarizes execution-contract presence, Phase 6 deployed field-validation posture, Phase 7 release posture, deployed smoke status, and live URL presence without changing runtime defaults or promotion decisions.

## Phase 8 Live URL Smoke Consistency Check

Phase 8 now also has a compact local consistency smoke artifact:

`docs/smoke/live-url-validation/phase8-live-url-smoke-consistency-check.json`

`docs/smoke/live-url-validation/phase8-live-url-smoke-consistency-check.md`

The smoke is read-only and local. It compares Phase 8 readiness fields with the corresponding handoff bundle row to expose evidence drift without calling deployed endpoints or changing runtime defaults.

## Phase 8 Live URL Validation Decision Record

Phase 8 now also has a live URL validation decision record for the current cycle:

`docs/operations/live-url-validation/phase8-live-url-validation-decision-record.md`

The record is documentation-only. It freezes current live-url validation verdict and open gates while preserving the boundary that runtime default promotion remains a separate decision gate.

## Phase 9 MyPrivateAgent Local Consumption Contract

Phase 9 now introduces a read-only local consumption contract for MyPrivateAgent:

`docs/integration/myprivateagent-local-consumption/phase9-myprivateagent-local-consumption-contract.md`

The contract defines local URL/access assumptions, required read-only discovery endpoints, and provider-vs-control-plane ownership boundaries without changing runtime defaults.

## Phase 9 MyPrivateAgent Local Consumption Readiness

Phase 9 now also has a machine-readable local-consumption readiness export:

`docs/integration/myprivateagent-local-consumption/phase9-myprivateagent-local-consumption-readiness.json`

`docs/integration/myprivateagent-local-consumption/phase9-myprivateagent-local-consumption-readiness.md`

The export is read-only and local. It summarizes contract presence, Phase 7/8 linkage, integration-probe posture, optional deployed smoke context, and open gates for local consumption review.

## Phase 9 MyPrivateAgent Local Consumption Smoke

Phase 9 now also has a compact local-consumption smoke artifact:

`docs/smoke/myprivateagent-local-consumption/phase9-myprivateagent-local-consumption-smoke.json`

`docs/smoke/myprivateagent-local-consumption/phase9-myprivateagent-local-consumption-smoke.md`

The smoke is read-only and local. It checks local-consumption contract coverage, control-plane compatibility, graph planned-boundary signal, and runtime-promotion boundary alignment without mutating provider state.

## Phase 9 MyPrivateAgent Local Consumption Decision Record

Phase 9 now also has a local-consumption decision record for the current cycle:

`docs/integration/myprivateagent-local-consumption/phase9-myprivateagent-local-consumption-decision-record.md`

The record is documentation-only. It freezes the current verdict for local MyPrivateAgent consumption review while preserving runtime-default and control-plane boundaries.

## Phase 10 MyPrivateAgent Local Consumer Verification Contract

Phase 10 introduces a caller-shaped, read-only local consumer verification contract:

`docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-verification-contract.md`

The contract keeps the recommended local URL at `http://127.0.0.1:8020`, keeps `PROVIDER_API_KEY` optional for local development, and defines the provider discovery flow a MyPrivateAgent-shaped consumer can inspect before real repository integration.

## Phase 10 MyPrivateAgent Local Consumer Readiness

Phase 10 now also has a machine-readable local consumer readiness export:

`docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-readiness.json`

`docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-readiness.md`

The export is read-only and local. It summarizes Phase 9 linkage, provider handoff posture, Phase 4 evidence-pack readiness, graph planned-boundary status, access-key posture, and runtime-promotion boundary status.

## Phase 10 MyPrivateAgent Local Consumer Probe

Phase 10 now also has a compact caller-shaped local consumer probe artifact:

`docs/smoke/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-probe.json`

`docs/smoke/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-probe.md`

The probe validates local access assumptions, contract coverage, handoff visibility, evidence-pack caller smoke, graph planned-boundary alignment, and runtime-default preservation without mutating provider state or requiring a live MyPrivateAgent integration.

## Phase 10 MyPrivateAgent Local Consumer Decision Record

Phase 10 now also has a local consumer verification decision record:

`docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-decision-record.md`

The record freezes the current `ready_for_local_myprivateagent_consumer_probe_review` posture while preserving provider/caller ownership boundaries and runtime-default gates.

## Phase 11 Local Provider Integration Dry-Run Contract

Phase 11 introduces a provider-side local integration dry-run contract:

`docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-contract.md`

The contract defines discovery, retrieval-consumption, and source-binding preview checks for a MyPrivateAgent-style local integration review while keeping the provider read-only and runtime-default boundaries unchanged.

## Phase 11 Local Provider Integration Profile

Phase 11 now has a local integration profile export:

`docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-profile.json`

`docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-profile.md`

The profile summarizes Phase 10 linkage, local URL and API-key mode assumptions, integration probe state, and handoff posture for local dry-run review.

## Phase 11 Local Provider Integration Smokes

Phase 11 also adds three compact smoke artifacts:

`docs/smoke/myprivateagent-local-provider-integration/phase11-provider-discovery-smoke.json`

`docs/smoke/myprivateagent-local-provider-integration/phase11-rag-retrieve-consumption-smoke.json`

`docs/smoke/myprivateagent-local-provider-integration/phase11-source-binding-preview-smoke.json`

These smokes validate discovery compatibility, retrieval-consumption evidence compatibility, and source-binding preview compatibility without mutating provider state.

## Phase 11 Local Provider Integration Decision Record

Phase 11 now also has a local integration decision record:

`docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-decision-record.md`

The record freezes `ready_for_local_provider_integration_review` while preserving caller-owned binding and policy boundaries.

## Phase 12 Open-Source RAG Engine Evaluation

Phase 12 records the current strategic selection boundary for mature open-source RAG engines:

`docs/roadmap/open_source_rag_engine_evaluation_roadmap.md`

The decision is `continue_provider_first_with_candidate_backends`. The short-term priority is smooth local MyPrivateAgent RAG consumption through the existing provider contract, evidence pack, handoff, source-binding preview, and local integration smoke artifacts. LlamaIndex remains the current lightweight baseline while Qdrant, BGE-M3, hybrid retrieval, pgvector, Haystack, RAGFlow, LightRAG, and GraphRAG-related options stay behind evidence-backed candidate gates.

This phase is intentionally strategy and evaluation oriented. It does not replace the provider with a platform, does not promote runtime defaults, does not add heavy parser dependencies, and does not move caller control-plane responsibilities into this project. Dify, Langflow, and RAGFlow-style platform capabilities remain product references or external integrations unless a separate evidence-backed change approves a narrow provider-owned backend capability.

### Phase 12a Local RAG Integration Hardening (Execution Slice)

Before any candidate backend migration, the first execution slice under Phase 12 is local MyPrivateAgent RAG integration hardening:

- normalize local URL and API-key mode assumptions,
- harden contract and evidence readiness outputs for local consumers,
- add a deterministic local hardening smoke for manifest, preflight, retrieval-consumption, source-binding preview, and phase4/phase10/phase11 linkage,
- keep all outputs read-only and keep `keep_runtime_defaults` as the default decision.

This keeps the project practical for immediate local integration while preserving long-term backend evaluation agility.

## Phase 13 Provider Roadmap Decision Checkpoint

Phase 13 is the next global decision slice after the Phase 12 candidate evidence chain.

Its job is to read the current Phase 12b through Phase 12f evidence, read the handoff posture, and choose the next small slice from a project-wide perspective rather than a pgvector-local momentum perspective.

The default recommendation is to resume provider integration hardening, keep pgvector candidate-only, and avoid opening a Phase 12g tuning loop unless fresh evidence clearly justifies it.

This phase is intentionally read-only and review-oriented. It does not promote runtime defaults, does not start a new backend benchmark loop, and does not move caller ownership boundaries into this project.

## Phase 14 MyPrivateAgent Provider Integration Acceptance Checkpoint

Phase 14 is the next acceptance slice after the Phase 10, Phase 11, and Phase 13 evidence chain.

Its job is to answer whether the provider is ready for a MyPrivateAgent repo-side trial from a project-wide perspective, using the existing local consumer, local provider integration, roadmap posture, and handoff evidence.

The default recommendation is to approve repo-side trial only when the provider evidence, handoff visibility, and local environment posture are all ready. When they are not, the checkpoint should classify the blocker explicitly so the next action stays obvious.

This phase is intentionally read-only and acceptance-oriented. It does not create source-to-agent binding, does not promote runtime defaults, does not change backend selection, and does not move caller control-plane ownership into this project.

## Phase 15 MyPrivateAgent Repo-Side Trial Dispatch Package

Phase 15 turns the Phase 10, Phase 11, Phase 13, and Phase 14 evidence chain into a caller-facing dispatch package that MyPrivateAgent can consume without stitching multiple reports together.

Its job is to tell the caller whether the provider is ready to dispatch a repo-side trial, what blocker category applies if it is not, and which follow-up actions should happen next. The package stays local, read-only, and provider-first.

The default recommendation is to dispatch the repo-side trial only when provider evidence, handoff visibility, and local environment posture are all ready. When they are not, the dispatch package should make the next action explicit instead of starting a trial or changing runtime defaults.

This phase is intentionally read-only and dispatch-oriented. It does not create source-to-agent binding, does not execute a repo-side trial, does not promote runtime defaults, does not change backend selection, and does not move caller control-plane ownership into this project.

## Phase 16 MyPrivateAgent Minimal Access Loop

Phase 16 turns the Phase 10, Phase 11, Phase 13, Phase 14, and Phase 15 evidence chain into a single caller-facing access loop report that MyPrivateAgent can use to decide whether the minimum access path is ready for a real repo-side trial.

Its job is to keep the access path small and explicit: the report should tell the caller whether the minimum loop is ready, which blocker category applies if it is not, and what the next action should be. The package stays local, read-only, and provider-first.

The default recommendation is to begin the repo-side trial only when provider evidence, handoff visibility, and local environment posture are all ready. When they are not, the access loop report should make the next action explicit instead of starting a trial or changing runtime defaults.

This phase is intentionally read-only and access-oriented. It does not create source-to-agent binding, does not execute a repo-side trial, does not promote runtime defaults, does not change backend selection, and does not move caller control-plane ownership into this project.

## Phase 17 Access-Focused Handoff Visibility

Phase 17 keeps the existing handoff bundle and refresh artifacts, but adds an access-focused visibility view so MyPrivateAgent can judge repo-side trial readiness without unrelated review-only evidence acting like a blocker.

Its job is to make the access path easier to read: the full bundle and refresh reports can remain review-level for broader operations evidence, while the access-focused view tells the caller whether the MyPrivateAgent chain itself is ready.

This phase is intentionally read-only and visibility-oriented. It does not delete unrelated evidence, does not create a new trial runner, does not promote runtime defaults, and does not move caller control-plane ownership into this project.

## Phase 18 MyPrivateAgent Access Gate Simplification

Phase 18 simplifies the MyPrivateAgent repo-side trial gate so the provider can stop extending the evidence chain and move toward real integration.

Its job is to separate primitive access blockers from review-only context. The primitive gate is limited to provider contract smoke, Phase 10 local consumer probe, Phase 11 provider discovery smoke, Phase 11 retrieve-consumption smoke, and Phase 11 source-binding preview smoke. Phase 10 readiness, Phase 11 profile, Phase 13 checkpoint, Phase 14 acceptance, Phase 15 dispatch, Phase 16 access loop, full handoff bundle, and handoff refresh remain visible as review context but do not block the minimal access gate by themselves.

This phase is intentionally read-only and gate-oriented. It does not execute the MyPrivateAgent repo-side trial, create source-to-agent binding, promote runtime defaults, change backend selection, or move caller control-plane ownership into this project.

After this phase, the evidence-chain work should stop expanding unless a real repo-side trial exposes a concrete provider bug. The next useful slice is Phase 19 MyPrivateAgent repo-side trial outcome capture, preferably driven from the MyPrivateAgent repository.

## Phase 24 Document RAG Trial Readiness Closure

Phase 24 closes the provider-side document RAG readiness question for a MyPrivateAgent repo-side trial:

`docs/integration/myprivateagent-document-rag-trial-readiness/phase24-document-rag-trial-readiness.json`

`docs/integration/myprivateagent-document-rag-trial-readiness/phase24-document-rag-trial-readiness.md`

The closure report intentionally reuses the simplified primitive access gate from Phase 18: provider contract smoke, Phase 10 local consumer probe, Phase 11 provider discovery smoke, Phase 11 retrieve-consumption smoke, and Phase 11 source-binding preview smoke. When those primitive signals are ready, Phase 24 returns `decision=go` even if older review-context reports remain visible as non-blocking notes.

This phase is read-only and provider-side. It does not execute the MyPrivateAgent trial, create source-to-agent binding, promote retrieval defaults, start live deployment validation, rebuild indexes, execute GraphRAG, or move caller control-plane ownership into this project. The next action is to begin the MyPrivateAgent repo-side document RAG trial and capture the outcome in the caller repository.

## Phase 25 MyPrivateAgent Live Trial Outcome Feedback Closure

Phase 25 records the result of a real MyPrivateAgent live trial from the provider side:

`docs/integration/myprivateagent-live-trial-outcome-feedback/phase25-myprivateagent-live-trial-outcome-feedback.json`

`docs/integration/myprivateagent-live-trial-outcome-feedback/phase25-myprivateagent-live-trial-outcome-feedback.md`

The report consumes an explicit MyPrivateAgent trial outcome JSON file and classifies provider follow-up as `no_provider_action_required`, `provider_review_required`, or `provider_blocked`. This is a feedback closure, not a new readiness chain. When the caller-side live trial succeeds with provider retrieve evidence, the provider access-readiness loop should close and future work should only proceed from concrete trial bugs, real corpus/parser demand, or separately approved backend promotion gates.

This phase is read-only and provider-side. It does not execute MyPrivateAgent code, call provider HTTP endpoints, create source-to-agent binding, promote retrieval defaults, start live deployment validation, rebuild indexes, execute GraphRAG, or move caller control-plane ownership into this project.

## Post-Access Workstream Rebaseline

After Phase 25, the access-readiness chain is closed for the current MyPrivateAgent document RAG trial path:

`docs/roadmap/provider-workstream-rebaseline/provider-workstream-rebaseline.json`

`docs/roadmap/provider-workstream-rebaseline/provider-workstream-rebaseline.md`

The rebaseline changes the project posture from sequential readiness phases to trigger-driven workstreams:

- MyPrivateAgent access readiness: `closed`
- Provider bugfix: `active_if_triggered` by real caller trial failures
- Corpus/parser expansion: `deferred` until real non-Markdown corpus demand appears
- Retrieval backend promotion: `candidate_only` until quality, citation, latency, deployment, and operations gates pass
- GraphRAG execution: `deferred` until relationship-heavy use cases and ownership are explicit
- Deployment operations: `active_if_triggered` by a deployment owner or real deployment environment

Future OpenSpec changes should declare their trigger condition rather than continuing the access-readiness phase chain. This avoids a Phase 26 readiness loop while keeping the provider ready to respond to concrete bugs, corpus needs, backend promotion evidence, deployment requests, or graph-heavy use cases.

## Local Usable Run Loop

The local run-loop is the day-1 check after a developer starts the provider with `uvicorn`:

```powershell
conda run -n GRAPHRAG python scripts/export_local_usable_run_loop.py `
  --base-url http://127.0.0.1:8020
```

It exports:

`docs/local-run/local-usable-run-loop.json`

`docs/local-run/local-usable-run-loop.md`

The report returns `go`, `review`, or `blocked` by checking the already-running local service through `/live`, `/ready`, `/health`, provider manifest, preflight, RAG retrieve, and RAG answer. It is intentionally local and lightweight: it does not start the server, download models, start Qdrant/pgvector, rebuild indexes, create source bindings, promote retrieval defaults, or execute GraphRAG.

## PDF Derived Markdown Corpus Trial

Raw PDF remains outside provider ingestion. A small local trial can still evaluate whether the first pages of a real PDF are useful RAG material by extracting text into a markdown artifact first:

```powershell
python scripts/export_pdf_derived_markdown_trial.py `
  --pdf-path "<local-pdf-path>" `
  --max-pages 5 `
  --query "公司主营业务是什么？"
```

The trial exports:

`docs/local-run/pdf-derived-corpus/company_profile_2025_trial.md`

`docs/local-run/pdf-derived-corpus/pdf-derived-markdown-trial.json`

`docs/local-run/pdf-derived-corpus/pdf-derived-markdown-trial.md`

This is a local corpus-quality probe, not parser promotion. It does not register raw PDF as a supported ingestion format, does not start OCR/Layout services, does not add PaddleOCR as a dependency, does not promote retrieval backends, and does not execute GraphRAG. If text extraction is insufficient, PaddleOCR or PP-Structure should remain external providers that produce derived text/markdown for the provider to consume later.

## Local Business Corpus Trial Loop

After a local markdown artifact exists, the next lightweight check is a pre-registration business corpus trial:

```powershell
python scripts/export_local_business_corpus_trial.py `
  --markdown-path docs/local-run/pdf-derived-corpus/company_profile_2025_trial.md `
  --source-id company_profile_2025_trial `
  --query "公司主营业务是什么？"
```

The trial exports:

`docs/local-run/business-corpus-trial/local-business-corpus-source.json`

`docs/local-run/business-corpus-trial/local-business-corpus-chunks.json`

`docs/local-run/business-corpus-trial/local-business-corpus-trial.json`

`docs/local-run/business-corpus-trial/local-business-corpus-trial.md`

This loop validates a markdown corpus before formal source registration. It can produce a `go`, `review`, or `blocked` decision over file presence, chunkability, retrieved evidence, and citation allowlist behavior. It does not mutate the default provider source catalog, expose the source through provider HTTP APIs, create source bindings, run formal ingestion jobs, persist index lifecycle state, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration.

## Local Corpus Caller Handoff

After a local business corpus trial returns `go`, the provider can export a caller-facing review package:

```powershell
python scripts/export_local_corpus_caller_handoff.py `
  --trial-report docs/local-run/business-corpus-trial/local-business-corpus-trial.json
```

The handoff exports:

`docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.json`

`docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.md`

The status `ready_for_caller_review` means the caller can inspect the source id, markdown artifact, overlay, chunks, generated citations, and trial boundaries before deciding whether to propose formal binding or source registration. It is not production registration and does not mutate source catalog, run ingestion jobs, create source bindings, execute MyPrivateAgent orchestration, promote retrieval backends, or execute GraphRAG.

## Approved Local Corpus Source Registration

After a local corpus handoff is `ready_for_caller_review`, the provider can explicitly register the markdown as an approved local source:

```powershell
python scripts/register_approved_local_corpus_source.py `
  --handoff docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.json
```

The registration writes:

`app/data/local_sources/approved_sources.json`

`app/data/sources/company_profile_2025_trial.md`

`docs/local-run/approved-local-source-registration/approved-local-source-registration.json`

`docs/local-run/approved-local-source-registration/approved-local-source-registration.md`

After registration, the source is visible through `GET /api/rag/sources`, has a source document manifest, and can be used by retrieve/answer requests. This is the local provider usability closure for a markdown corpus. It does not create source-to-agent binding, create formal ingestion jobs, start OCR services, promote Qdrant/BGE/hybrid/reranker defaults, execute MyPrivateAgent orchestration, or execute GraphRAG.

## Approved Local Corpus Acceptance Smoke

After a local corpus is registered, the provider can export a business acceptance smoke:

```powershell
python scripts/export_approved_local_corpus_acceptance_smoke.py `
  --source-id company_profile_2025_trial
```

The smoke writes:

`docs/local-run/approved-local-corpus-acceptance/approved-local-corpus-acceptance-smoke.json`

`docs/local-run/approved-local-corpus-acceptance/approved-local-corpus-acceptance-smoke.md`

The smoke validates catalog visibility, source document manifest availability, multiple answerable company-profile questions, citation allowlist behavior, and an unrelated negative-control query. It returns `go`, `review`, or `blocked` so the team can decide whether the registered local corpus is ready for MyPrivateAgent-side trial usage. It runs in-process and does not start external services, register sources, create source-to-agent binding, create formal ingestion jobs, start OCR, promote retrieval backends, call vector databases, or execute GraphRAG.

## Provider API Access Guard

Phase 6 deployment work now includes a default-off provider API key guard. When `PROVIDER_API_KEY` is configured, `/api/*` requests require either:

```text
Authorization: Bearer <token>
X-Provider-Api-Key: <token>
```

`GET /health` remains public for deployment health checks.

This is a lightweight component access guard, not an identity or policy system. MyPrivateAgent or another external control plane still owns user identity, roles, approvals, audit policy, source-to-agent binding, and final answer policy.

Provider manifest access metadata now advertises the same component access contract in machine-readable form: public health path, protected API path pattern, accepted header schemes, whether an API key is configured, and an explicit boundary note. Secret values are never included in the manifest.

## Lightweight Deployment Profile

Phase 6 now includes a minimal container deployment profile:

```text
Dockerfile
docker-compose.example.yml
.env.example
.dockerignore
```

The profile starts `uvicorn app.main:app` on port `8020`, exposes a `/health` health check, mounts source documents, index lifecycle state, and model artifacts as runtime directories, and keeps fixture/mock defaults unless operators explicitly opt into Qdrant or local embedding models.

The image build intentionally excludes local model artifacts, index state, generated benchmark/evidence reports, and tests. It does not download models, start Qdrant, enable GraphRAG, add TLS termination, configure reverse proxies, or manage secrets. Those remain deployment-owner or external control-plane responsibilities.

## Deployed Provider Smoke

Phase 6 now includes a deployed HTTP smoke probe for already-running provider components:

```powershell
conda run -n GRAPHRAG python scripts/export_deployed_provider_smoke.py `
  --base-url http://127.0.0.1:8020
```

The probe calls only:

- `GET /health`
- `GET /api/provider/manifest`
- `GET /api/provider/preflight`
- `GET /api/provider/source-bindings`
- `GET /api/provider/handoff`

It supports an optional provider API key through `PROVIDER_API_KEY` or `--provider-api-key` and writes evidence under `docs/integration/deployed-provider-smoke/`. This validates network reachability, component access guard compatibility, provider identity, bindability, live source binding review reachability, and handoff evidence status after deployment.

It remains a lightweight provider-component smoke, not platform certification. It does not execute retrieval, answer composition, ingestion, index rebuilds, embedding models, vector databases, model downloads, GraphRAG, TLS termination, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy.

The provider handoff bundle summarizes deployed smoke as optional Phase 6 evidence. Missing deployed smoke keeps the bundle in `review` with `run_deployed_provider_smoke_after_deployment`; present `ready` or `review` deployed evidence is surfaced directly, and present `blocked` deployed evidence blocks the bundle. This keeps local development lightweight while making live URL evidence visible from the same handoff entry point used by external control planes.

Deployed smoke now includes source binding review as a protected API check. It summarizes source count, bindable source count, source status counts, and recommended action counts, and fails closed when source binding evidence is blocked or invalid. This validates live binding-review reachability without creating source-to-agent bindings or executing retrieval, ingestion, answer composition, or GraphRAG.

## Deployed Field Validation Readiness

Phase 6 now also has a local deployed field-validation readiness export that summarizes the deployment-readiness report, handoff bundle posture, and deployed smoke evidence into a single read-only review artifact:

`docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.json`

`docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.md`

The export is intentionally read-only. It does not replace deployed smoke, and it does not change runtime defaults. It only makes the live URL review posture easier to inspect from the same handoff-oriented evidence flow used by optional deployed smoke.

Phase 6 now also has a local deployed handoff consistency smoke that compares the deployed field-validation readiness export with the provider handoff bundle:

`docs/smoke/deployed-field-validation/phase6-deployed-handoff-consistency-smoke.json`

`docs/smoke/deployed-field-validation/phase6-deployed-handoff-consistency-smoke.md`

The smoke is intentionally read-only. It keeps the deployed field-validation posture easy to audit without turning the provider into a live deployment verifier.

Phase 6 now also has a local deployed field-validation decision record that freezes the current live-url verdict and open gates:

`docs/operations/deployed-field-validation/phase6-deployed-field-validation-decision-record.md`

The record is intentionally documentation-only. It does not switch runtime defaults, and it exists to make the current live-url posture easy to reference from handoff and operations review.

## Source Binding Summary

Phase 2 and Phase 6 now connect through a read-only source binding summary:

```text
GET /api/provider/source-bindings
```

The summary combines configured source catalog facts, source package context, retrieval backend readiness, index lifecycle status, source document fingerprint drift, ingestion preflight status, citation anchor count, chunk manifest count, parser-ready document count, unsupported document count, and deterministic recommended actions. It helps MyPrivateAgent or another external control plane decide whether a source is ready for binding without reading several provider diagnostics separately.

This remains provider-owned evidence, not binding policy. The provider does not create source-to-agent bindings, run approvals, write audit records, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding/vector stores, or execute GraphRAG from this endpoint.

Source binding summary is also promoted as a formal provider capability: `knowledge.provider.source_bindings`. This makes binding readiness evidence discoverable through `/api/capabilities`, provider manifest capability ids, and default provider preflight requirements while preserving external ownership of actual source-to-agent binding decisions.

Source binding summary can also be exported as handoff evidence:

```powershell
conda run -n GRAPHRAG python scripts/export_provider_source_bindings.py
```

The handoff refresh workflow regenerates this evidence before the final provider handoff bundle, and the handoff bundle treats it as required local evidence. This makes source bindability visible in the same evidence package used for MyPrivateAgent review while still leaving actual source-to-agent binding policy outside this provider.

Source binding coverage counts are informational evidence. They reuse existing source manifest and ingestion preflight diagnostics, do not change binding decisions by themselves, and do not add parsers, indexing execution, retrieval execution, answer composition, or GraphRAG.

Source binding package context is also informational evidence. It reuses existing `source_package` metadata such as domain, language, sensitivity, supported formats, and citation granularity so external control planes can review business fit before binding. It does not implement sensitivity-based approval, authorization policy, audit, parser expansion, ingestion execution, retrieval execution, answer composition, or GraphRAG.

Provider handoff evidence now summarizes source binding status counts and recommended action counts from the existing source binding report. This gives MyPrivateAgent or another external control plane a compact view of whether sources are ready, reviewable, or blocked before opening the full binding evidence. It remains read-only and does not create bindings, change binding policy, regenerate evidence, run ingestion, execute retrieval, compose answers, or execute GraphRAG.

The source binding endpoint itself now exposes the same compact aggregate counts: total source count, bindable source count, source status counts, and recommended action counts. These counts are derived from existing source binding rows so callers can make a quick integration decision without duplicating row aggregation logic. They remain evidence-only and do not create bindings, change binding policy, run approvals, write audit records, run ingestion, execute retrieval, compose answers, or execute GraphRAG.

Provider handoff and deployed smoke summaries now prefer those provider-owned aggregate counts when present, while retaining row-based fallback for older evidence. This keeps the evidence chain consistent without changing binding decisions, runtime defaults, source readiness rules, or caller-owned control-plane responsibilities.
