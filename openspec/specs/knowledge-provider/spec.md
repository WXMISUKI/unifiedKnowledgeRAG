# knowledge-provider Specification

## Purpose
TBD - created by archiving change add-knowledge-provider-v1. Update Purpose after archive.
## Requirements
### Requirement: Provider health reports machine-readable readiness
The system SHALL expose provider health with machine-readable service, RAG, answer composer, graph, document retrieval backend, and source index lifecycle readiness fields.

#### Scenario: Provider health is ready
- **WHEN** a caller requests `GET /health`
- **THEN** the response includes `status`, `service`, `rag.status`, `rag.backend`, `rag.backend_status`, `rag.index_status`, `answer.status`, `answer.backend`, `answer.backend_status`, and `graph.status`

#### Scenario: Document retrieval backend is degraded
- **WHEN** the configured document retrieval backend cannot load its index lifecycle status
- **THEN** `GET /health` reports provider `status=degraded` and includes a machine-readable RAG degradation reason

#### Scenario: Answer composer is degraded
- **WHEN** the configured answer composer is unavailable
- **THEN** `GET /health` reports provider `status=degraded` and includes a machine-readable answer degradation reason

### Requirement: Provider capabilities expose stable knowledge capability ids
The system SHALL expose stable capability identifiers and optional status reason and invocation metadata, including request and response schema references when available, for document RAG retrieval, document RAG cited answer orchestration, and graph query boundaries while keeping production infrastructure choices behind explicit architecture decision records.

#### Scenario: Capabilities are discoverable
- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.retrieve`, `knowledge.rag.answer`, and `knowledge.graph.query` capability ids with machine-readable status and HTTP invocation metadata

#### Scenario: Retrieval capability is invokable
- **WHEN** a caller inspects the `knowledge.rag.retrieve` capability
- **THEN** its invocation metadata identifies `POST /api/rag/retrieve` and references the retrieval request and response schemas

#### Scenario: Answer capability is invokable
- **WHEN** a caller inspects the `knowledge.rag.answer` capability
- **THEN** its invocation metadata identifies `POST /api/rag/answer` and references the answer request and response schemas

#### Scenario: Answer composer is not ready
- **WHEN** the configured answer composer is unavailable
- **THEN** the `knowledge.rag.answer` capability status is `degraded` and includes a reason

#### Scenario: Graph query is planned
- **WHEN** a caller inspects the `knowledge.graph.query` capability
- **THEN** its status is `planned` and includes a reason

#### Scenario: Production infrastructure is not yet selected
- **WHEN** embedding model, vector database, queue worker, reranker, graph storage, or production answer composer choices are still open
- **THEN** provider capabilities remain provider-neutral and do not expose implementation-specific dependency details as API contracts

### Requirement: Catalog exposes source readiness

The system SHALL expose a source catalog that lists knowledge bases and graph namespaces with stable ids, status, owners, version metadata, backend readiness metadata, and durable source index lifecycle metadata.

#### Scenario: Catalog lists configured sources

- **WHEN** a caller requests `GET /api/catalog`
- **THEN** the response includes `knowledge_bases` and `graphs` arrays with stable source ids, readiness status, document retrieval backend metadata, and source index lifecycle status loaded from the local lifecycle store

### Requirement: Graph schema boundary is explicit

The system SHALL expose graph schema metadata separately from document RAG retrieval.

#### Scenario: Graph schemas are discoverable

- **WHEN** a caller requests `GET /api/graph/schemas`
- **THEN** the response includes graph ids and serializable schema metadata

### Requirement: Graph query boundary returns structured status

The system SHALL expose a graph query endpoint that returns serializable graph result envelopes or structured provider errors.

#### Scenario: Graph query is not implemented in first slice

- **WHEN** a caller requests `POST /api/graph/query` during the document-RAG-only slice
- **THEN** the response uses a structured error code that states graph query execution is not implemented

### Requirement: Provider errors expose machine-readable details
The system SHALL include optional machine-readable details on structured provider errors without changing existing error codes or messages.

#### Scenario: Unknown RAG source error includes details
- **WHEN** a caller requests document RAG retrieval or answer with unknown knowledge base ids
- **THEN** the provider error includes `details.requested_source_ids` and `details.unknown_source_ids`

#### Scenario: Not-ready RAG index error includes details
- **WHEN** a caller requests document RAG retrieval or answer for a source whose index is not ready
- **THEN** the provider error includes `details.requested_source_ids`, `details.not_ready_source_ids`, and `details.retrieval_backend`

#### Scenario: Answer composer error includes details
- **WHEN** the configured answer composer is unsupported or not implemented
- **THEN** the provider error includes the configured composer, configured model, and supported composer names

#### Scenario: Graph query not implemented error includes details
- **WHEN** a caller requests `POST /api/graph/query` before GraphRAG execution is implemented
- **THEN** the provider error includes the requested graph id, planned status, and graph capability id

#### Scenario: Existing error envelope is preserved
- **WHEN** provider error details are added
- **THEN** existing `ok=false`, `result=null`, `error.code`, and `error.message` behavior remains compatible

### Requirement: Provider exposes executable contract smoke evidence
The system SHALL provide a local executable smoke report that validates the provider health, capability invocation metadata, document RAG retrieval, cited answer orchestration, and planned graph query boundary without requiring an external server.

#### Scenario: Smoke report passes for default provider configuration
- **WHEN** the smoke report is generated with the default local provider configuration
- **THEN** the report marks itself as passed and includes successful checks for health, capabilities, document retrieval, cited answer, and graph planned boundary behavior

#### Scenario: Smoke report includes integration-critical metadata
- **WHEN** the smoke report validates document retrieval and cited answer endpoints
- **THEN** the report includes evidence that retrieval trace metadata, request filter context metadata, answer trace metadata, and citations are present

#### Scenario: Smoke report covers insufficient-evidence evidence packs
- **WHEN** the smoke report validates a query with no matching RAG evidence
- **THEN** the report includes evidence that retrieval and answer envelopes expose `evidence_pack.status=insufficient_evidence`, `reason=no_documents`, zero evidence count, and no allowed citations

#### Scenario: Smoke evidence can be exported
- **WHEN** a caller runs the provider contract smoke export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files without changing provider HTTP API contracts

### Requirement: Provider contract smoke validates graph schema discovery

The system SHALL validate graph schema discovery in provider contract smoke separately from planned graph query execution.

#### Scenario: Contract smoke checks graph schemas

- **WHEN** provider contract smoke runs
- **THEN** it calls `GET /api/graph/schemas` and records configured graph ids and graph metadata counts

#### Scenario: Contract smoke preserves planned graph query boundary

- **WHEN** provider contract smoke validates graph schema discovery
- **THEN** it still validates `POST /api/graph/query` as a planned not-implemented boundary rather than executable GraphRAG

#### Scenario: Graph schema contract smoke remains read-only

- **WHEN** provider contract smoke checks graph schemas
- **THEN** it does not execute graph queries, connect to graph stores, create ingestion jobs, extract entities, build ontology workflows, rebuild indexes, execute retrieval, or compose answers

### Requirement: Provider smoke covers insufficient-evidence evidence packs
The provider contract smoke report SHALL validate that RAG retrieval and cited answer envelopes fail closed with machine-readable evidence pack diagnostics when no supporting evidence is returned.

#### Scenario: Smoke checks insufficient-evidence retrieval pack
- **WHEN** the provider contract smoke runs against a query with no matching evidence
- **THEN** the smoke report verifies the retrieval response has `ok=true`, no documents, no allowed citations, and `result.metadata.evidence_pack.status=insufficient_evidence`

#### Scenario: Smoke checks insufficient-evidence answer pack
- **WHEN** the provider contract smoke runs the answer endpoint against the same query with no matching evidence
- **THEN** the smoke report verifies the answer response has `ok=true`, `result.answer_status=insufficient_evidence`, no answer citations, and `result.metadata.evidence_pack.reason=no_documents`

#### Scenario: Smoke report remains local and read-only
- **WHEN** insufficient-evidence pack smoke is executed
- **THEN** it does not start ingestion jobs, rebuild indexes, call embedding models, call vector databases, or execute graph queries

### Requirement: Evidence pack includes provenance metadata
The system SHALL include provider-owned provenance metadata in RAG evidence pack entries when the retrieval backend knows it.

#### Scenario: Retrieved evidence includes provenance
- **WHEN** a caller requests `POST /api/rag/retrieve` and documents are returned
- **THEN** each `metadata.evidence_pack.evidence` entry includes provenance fields for source path, chunk id, chunking strategy, and citation anchor when available

#### Scenario: Answer evidence includes provenance
- **WHEN** a caller requests `POST /api/rag/answer` and evidence is returned
- **THEN** the answer metadata evidence pack includes the same provenance metadata as retrieval for the returned evidence

#### Scenario: Public document envelope remains stable
- **WHEN** provenance metadata is added to evidence packs
- **THEN** the top-level returned `documents` entries retain their existing source id, document id, title, snippet, score, and citation contract

#### Scenario: Empty evidence pack remains explicit
- **WHEN** retrieval returns no documents
- **THEN** the evidence pack remains `insufficient_evidence` with an empty evidence list and no fabricated provenance

### Requirement: Provider exposes integration manifest
The system SHALL expose a read-only provider integration manifest for external control planes that need to discover provider identity, component role, contract version, key endpoint paths, and supported knowledge capability ids before invoking provider capabilities.

#### Scenario: Manifest exposes provider identity and role
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the response includes provider id, provider name, provider version, manifest version, contract version, component role, and compatible control-plane metadata

#### Scenario: Manifest references integration endpoints
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the response includes stable paths for health, capabilities, OpenAPI schema, provider contract smoke evidence, and core RAG and graph capability endpoints

#### Scenario: Manifest lists supported capability ids
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the response includes `knowledge.rag.retrieve`, `knowledge.rag.answer`, and `knowledge.graph.query` as supported capability ids without exposing provider implementation internals as binding contracts

#### Scenario: Manifest is side-effect free
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the provider does not start ingestion jobs, rebuild indexes, call embedding models, call vector databases, or execute graph queries

### Requirement: Provider exposes separate liveness and readiness probes
The system SHALL expose lightweight liveness and readiness probes for high-availability deployments while keeping `/health` compatible.

#### Scenario: Liveness probe is side-effect free
- **WHEN** a caller requests `GET /live`
- **THEN** the response reports the provider process as live without constructing retrieval backends, checking indexes, running answer readiness, executing ingestion, calling vector stores, or executing GraphRAG

#### Scenario: Readiness probe reports traffic readiness
- **WHEN** a caller requests `GET /ready`
- **THEN** the response includes the same machine-readable readiness details as `/health` for service, RAG, answer, and graph status

#### Scenario: Degraded readiness fails HTTP
- **WHEN** a caller requests `GET /ready` and the readiness body has `status=degraded`
- **THEN** the endpoint returns HTTP 503 with the same readiness response body for diagnostics

#### Scenario: Health endpoint remains compatible
- **WHEN** a caller requests `GET /health`
- **THEN** the endpoint continues to return the existing readiness response shape

#### Scenario: Manifest advertises operational probes
- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `live` and `ready` paths for external discovery

### Requirement: Provider exposes binding preflight
The system SHALL expose a read-only provider preflight endpoint that summarizes whether the provider is currently bindable by an external control plane using the provider manifest, health readiness, capability coverage, and schema-reference coverage.

#### Scenario: Preflight passes for default local provider
- **WHEN** a caller requests `GET /api/provider/preflight` with the default local provider configuration
- **THEN** the response marks `bindable=true`, includes provider id and contract version, and includes passed checks for manifest, health, required capabilities, and schema references

#### Scenario: Preflight reports degraded readiness
- **WHEN** provider health is degraded
- **THEN** the preflight response marks `bindable=false` and includes a failed health readiness check with machine-readable details

#### Scenario: Preflight includes planned graph boundary
- **WHEN** graph query execution remains planned
- **THEN** the preflight response still includes `knowledge.graph.query` in required capability coverage while preserving its planned capability status in details

#### Scenario: Preflight is side-effect free
- **WHEN** a caller requests `GET /api/provider/preflight`
- **THEN** the provider does not start ingestion jobs, rebuild indexes, call document retrieval, call answer composition, call embedding models, call vector databases, or execute graph queries

### Requirement: Provider preflight accepts caller requirements
The system SHALL allow callers to supply binding requirements to provider preflight so an external control plane can fail closed on incompatible contract versions or missing capabilities.

#### Scenario: Required contract version matches
- **WHEN** a caller requests `GET /api/provider/preflight` with `required_contract_version=knowledge-provider-contract-v1`
- **THEN** the response includes a passed contract version check and remains bindable when other checks pass

#### Scenario: Required contract version mismatches
- **WHEN** a caller requests `GET /api/provider/preflight` with an unsupported `required_contract_version`
- **THEN** the response marks `bindable=false` and includes a failed contract version check with requested and actual contract versions

#### Scenario: Required capabilities match
- **WHEN** a caller requests `GET /api/provider/preflight` with repeated `required_capability_ids` that are all supported
- **THEN** required capability and schema-reference checks use the requested capability ids and pass when those capabilities expose schema references

#### Scenario: Required capability is missing
- **WHEN** a caller requests `GET /api/provider/preflight` with an unsupported required capability id
- **THEN** the response marks `bindable=false` and includes the missing capability id in machine-readable details

#### Scenario: Default preflight remains compatible
- **WHEN** a caller requests `GET /api/provider/preflight` without explicit requirements
- **THEN** the provider uses the default required knowledge capability ids and current contract version checks

### Requirement: Provider preflight summarizes graph boundary schemas

The system SHALL include compact graph schema discovery details in provider preflight graph boundary evidence without executing graph queries.

#### Scenario: Preflight summarizes graph namespaces

- **WHEN** a caller requests `GET /api/provider/preflight`
- **THEN** the `graph_boundary` check details include graph schema count and configured graph ids

#### Scenario: Preflight preserves planned graph execution

- **WHEN** graph schemas are summarized in provider preflight
- **THEN** the `graph_boundary` check still reports graph query execution as planned until GraphRAG execution is separately approved

#### Scenario: Graph boundary preflight remains read-only

- **WHEN** provider preflight summarizes graph schemas
- **THEN** it does not execute graph queries, connect to graph stores, create ingestion jobs, extract entities, build ontology workflows, rebuild indexes, execute retrieval, or compose answers

### Requirement: Provider capability invocations include example requests
The system SHALL include provider-owned example request payloads in capability invocation metadata for stable knowledge capability ids so external control planes can construct first-call probes without relying on implementation-specific defaults.

#### Scenario: Retrieval capability includes an example request
- **WHEN** a caller inspects the `knowledge.rag.retrieve` capability from `GET /api/capabilities`
- **THEN** its invocation metadata includes an `example_request` with a query, at least one knowledge base id, a bounded `top_k`, and integration filter context

#### Scenario: Answer capability includes an example request
- **WHEN** a caller inspects the `knowledge.rag.answer` capability from `GET /api/capabilities`
- **THEN** its invocation metadata includes an `example_request` compatible with the cited answer request schema

#### Scenario: Graph capability example preserves planned boundary
- **WHEN** a caller inspects the `knowledge.graph.query` capability from `GET /api/capabilities`
- **THEN** its invocation metadata includes an `example_request` compatible with the graph query request schema while the capability status remains `planned`

#### Scenario: Invocation examples remain provider neutral
- **WHEN** invocation examples are exposed
- **THEN** they do not expose embedding model, vector database, reranker, graph store, or answer composer implementation details as API contracts

### Requirement: Provider integration probe supports external control-plane binding
The system SHALL provide a local read-only integration probe that external control planes can use as a reference binding flow for provider manifest, preflight, and capability discovery.

#### Scenario: Integration probe passes for default provider
- **WHEN** the integration probe runs against the default local provider with the current contract version and stable knowledge capability ids
- **THEN** it returns a machine-readable report with `bindable=true`, provider identity, manifest version, contract version, capability ids, capability statuses, invocation paths, and example request coverage

#### Scenario: Integration probe fails closed on incompatible requirements
- **WHEN** the integration probe is run with an unsupported required contract version or required capability id
- **THEN** it returns `bindable=false` and includes preflight check details that identify the incompatible requirement

#### Scenario: Integration probe is read-only
- **WHEN** the integration probe runs
- **THEN** it does not execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

#### Scenario: Integration probe preserves invocation examples
- **WHEN** the integration probe collects capability metadata
- **THEN** it includes each requested capability invocation and provider-owned example request without executing the example request

### Requirement: Provider integration probe evidence can be exported
The system SHALL provide a local export command for provider integration probe evidence so external control planes can persist machine-readable and human-readable provider binding results.

#### Scenario: Integration probe evidence exports for default provider
- **WHEN** a caller runs the provider integration probe export command with the default local provider configuration
- **THEN** the system writes JSON and Markdown files that include provider identity, contract version, requested binding requirements, bindable status, preflight checks, capability binding statuses, invocation paths, and example request coverage

#### Scenario: Integration probe export fails closed
- **WHEN** the integration probe report is not bindable
- **THEN** the export command still writes evidence files and exits with a failure status

#### Scenario: Integration probe export remains read-only
- **WHEN** the integration probe export command runs
- **THEN** it does not execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

#### Scenario: Integration probe Markdown is reviewable
- **WHEN** the integration probe Markdown report is rendered
- **THEN** it summarizes provider identity, bindability, preflight checks, capability ids, statuses, invocation paths, and example request coverage without embedding full request payloads

### Requirement: Provider deployment readiness evidence can be exported
The system SHALL provide a local deployment readiness export that summarizes whether the provider is ready for local binding review and future deployment planning without requiring an external server.

#### Scenario: Readiness export includes core checks
- **WHEN** the deployment readiness export runs
- **THEN** the report includes provider health status, provider preflight bindability, provider contract smoke status, and a combined readiness status

#### Scenario: Readiness export includes configuration review
- **WHEN** the deployment readiness export runs
- **THEN** the report includes retrieval backend, embedding provider, embedding model, answer composer, Qdrant collection settings, and source/index paths without exposing secret values

#### Scenario: Readiness export remains local and read-only
- **WHEN** deployment readiness is exported
- **THEN** it does not start ingestion jobs, rebuild indexes, download models, call embedding services, call vector databases, or execute graph queries

#### Scenario: Readiness evidence writes review artifacts
- **WHEN** a caller runs the deployment readiness export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files

### Requirement: Provider discovery exposes source document diagnostics

The provider discovery surface SHALL expose the document source manifest diagnostic capability so external control planes can discover and preflight it before binding.

#### Scenario: Manifest includes source document route template

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include a route template for `GET /api/rag/sources/{source_id}/documents`

#### Scenario: Capabilities include source document diagnostics

- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.source_documents` with a GET invocation, path template, response schema reference, and example source id

#### Scenario: Preflight validates diagnostic capability

- **WHEN** provider preflight runs with default required capability ids
- **THEN** it includes `knowledge.rag.source_documents` in requested capability ids and validates it without requiring a request body schema

#### Scenario: Provider smoke covers diagnostic discovery

- **WHEN** provider contract smoke runs
- **THEN** it verifies manifest and capability metadata for the source document diagnostics surface without executing retrieval, ingestion, or graph work

### Requirement: Provider handoff bundle evidence can be exported
The system SHALL provide a local provider handoff bundle export so external control planes and deployment reviewers can inspect provider identity, contract version, integration evidence, and operations evidence from one review artifact.

#### Scenario: Handoff bundle includes provider identity
- **WHEN** the provider handoff bundle export runs
- **THEN** the report includes provider id, provider name, provider version, contract version, manifest version, and generated timestamp

#### Scenario: Handoff bundle summarizes required evidence artifacts
- **WHEN** the provider handoff bundle export runs
- **THEN** the report includes provider integration probe, provider contract smoke, deployment readiness, and reindex readiness artifact rows with paths, presence, status, summaries, and recommended actions

#### Scenario: Handoff bundle fails closed on missing evidence
- **WHEN** a required evidence artifact is missing
- **THEN** the report marks the artifact as missing, marks the bundle status as `blocked`, and recommends regenerating the missing artifact

#### Scenario: Handoff bundle remains read-only
- **WHEN** the provider handoff bundle export runs
- **THEN** it does not regenerate prerequisite reports, call provider HTTP endpoints, execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

#### Scenario: Handoff bundle writes review artifacts
- **WHEN** a caller runs the provider handoff bundle export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files

### Requirement: Provider handoff bundle includes optional deployed smoke evidence

The system SHALL include deployed provider smoke evidence in the provider handoff bundle as optional deployment evidence without requiring a running external provider URL during local handoff generation.

#### Scenario: Missing deployed smoke is reviewable

- **WHEN** the provider handoff bundle is generated and deployed provider smoke evidence is missing
- **THEN** the bundle includes a deployed smoke artifact row with `present=false`, `status=review`, and a recommended action to run deployed smoke after deployment

#### Scenario: Ready deployed smoke is summarized

- **WHEN** deployed provider smoke evidence exists with `status=ready`
- **THEN** the handoff bundle includes it with `status=ready` and summarizes the deployed base URL and handoff status

#### Scenario: Review deployed smoke is preserved

- **WHEN** deployed provider smoke evidence exists with `status=review`
- **THEN** the handoff bundle keeps the overall bundle reviewable rather than marking it ready

#### Scenario: Blocked deployed smoke blocks handoff

- **WHEN** deployed provider smoke evidence exists with `status=blocked`
- **THEN** the handoff bundle marks the deployed smoke row blocked and marks the overall bundle blocked

#### Scenario: Handoff bundle remains read-only

- **WHEN** the provider handoff bundle is generated
- **THEN** it does not run deployed smoke, call provider HTTP endpoints, execute retrieval or answer composition, create ingestion jobs, rebuild indexes, call embedding models, call vector databases, or execute GraphRAG

### Requirement: Provider handoff summarizes source binding actions

The system SHALL include compact source status and recommended action rollups when the provider handoff bundle summarizes existing source binding evidence.

#### Scenario: Handoff summarizes source binding statuses

- **WHEN** the provider handoff bundle reads present source binding summary evidence
- **THEN** the `source_binding_summary` artifact summary includes counts for source binding row statuses

#### Scenario: Handoff summarizes source binding recommended actions

- **WHEN** the provider handoff bundle reads present source binding summary evidence
- **THEN** the `source_binding_summary` artifact summary includes counts for source binding recommended actions

#### Scenario: Handoff source binding action summary remains read-only

- **WHEN** source binding status and action counts are summarized in provider handoff evidence
- **THEN** the provider does not regenerate evidence, call provider HTTP endpoints, create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG

### Requirement: Provider handoff evidence can be refreshed locally
The system SHALL provide a local refresh command that regenerates provider handoff prerequisite evidence and the provider handoff bundle in a deterministic order for external control-plane review.

#### Scenario: Handoff evidence refresh runs prerequisite exporters
- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it regenerates provider integration probe, provider contract smoke, deployment readiness, reindex readiness, and provider handoff bundle artifacts in that order

#### Scenario: Handoff evidence refresh writes a summary report
- **WHEN** the provider handoff evidence refresh command completes
- **THEN** it writes machine-readable JSON and human-readable Markdown summary files that include each refresh step, output paths, status, and recommended action

#### Scenario: Handoff evidence refresh fails closed
- **WHEN** a refresh step fails or returns blocked evidence
- **THEN** the refresh summary marks the overall status as `blocked` and identifies the failing step

#### Scenario: Handoff evidence refresh preserves review state
- **WHEN** all refresh steps complete but one regenerated report requires review
- **THEN** the refresh summary marks the overall status as `review` rather than `ready`

#### Scenario: Handoff evidence refresh remains local
- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it does not start a server, add HTTP endpoints, create ingestion jobs, explicitly rebuild indexes, download models, call vector databases, or execute GraphRAG

### Requirement: Provider exposes read-only handoff bundle API

The system SHALL expose the current provider handoff bundle through a read-only HTTP endpoint so external control planes can inspect provider identity, contract version, integration evidence, and operations evidence without reading local files directly.

#### Scenario: Handoff endpoint returns bundle status

- **WHEN** a caller requests `GET /api/provider/handoff`
- **THEN** the response includes the handoff bundle id, status, provider identity, required evidence artifact rows, and operation notes

#### Scenario: Handoff endpoint is advertised by manifest

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `provider_handoff` with the path `/api/provider/handoff`

#### Scenario: Handoff endpoint fails closed on missing evidence

- **WHEN** a required handoff evidence artifact is missing
- **THEN** the endpoint response marks the artifact as `missing`, marks the bundle status as `blocked`, and recommends regenerating the missing artifact

#### Scenario: Handoff endpoint is side-effect free

- **WHEN** a caller requests `GET /api/provider/handoff`
- **THEN** the provider does not regenerate prerequisite reports, execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, or graph queries

### Requirement: Provider exposes source binding summary

The system SHALL expose a read-only source binding summary for external control planes to review configured knowledge source bindability, source package context, and binding evidence coverage before making source-to-agent binding decisions.

#### Scenario: Source binding summary lists configured sources

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the response includes each configured knowledge base with source id, owner, source status, source domain, language, sensitivity, supported formats, citation granularity, retrieval backend, backend status, index status, document count, citation anchor count, chunk manifest count, parser-ready document count, unsupported document count, drift statuses, bindability, and recommended action

#### Scenario: Ready source is bindable

- **WHEN** a source has ready catalog status, ready retrieval backend, ready index status, in-sync document fingerprints, and ready ingestion preflight
- **THEN** the source binding row marks `bindable=true`, `status=ready`, and recommends `bind_source_from_control_plane`

#### Scenario: Package context fields are informational

- **WHEN** a source binding row includes domain, language, sensitivity, supported formats, and citation granularity
- **THEN** those fields summarize existing source package diagnostics without changing binding decisions by themselves

#### Scenario: Coverage fields are informational

- **WHEN** a source binding row includes citation, chunk, and parser coverage counts
- **THEN** those fields summarize existing manifest and preflight diagnostics without changing binding decisions by themselves

#### Scenario: Drifted source is blocked

- **WHEN** a source document fingerprint is `changed` or `missing`
- **THEN** the source binding row marks `bindable=false`, `status=blocked`, and recommends repairing or reingesting the source before binding

#### Scenario: Summary is advertised by manifest

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `source_bindings` with the path `/api/provider/source-bindings`

#### Scenario: Source binding summary is read-only

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the provider does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG

### Requirement: Source binding summary evidence can be exported

The system SHALL provide a local export command for source binding summary evidence so deployment reviewers and external control planes can inspect source bindability, source package context, and binding evidence coverage from persisted handoff artifacts.

#### Scenario: Source binding evidence export writes artifacts

- **WHEN** a caller runs the source binding evidence export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown files containing source bindability status, source package context, coverage counts, recommended actions, and operation notes

#### Scenario: Source binding evidence participates in handoff bundle

- **WHEN** the provider handoff bundle is generated
- **THEN** it includes source binding evidence as a required local artifact and summarizes ready, review, blocked, or missing evidence states

#### Scenario: Handoff refresh regenerates source binding evidence

- **WHEN** the provider handoff evidence refresh command runs
- **THEN** it regenerates source binding evidence before regenerating the provider handoff bundle

#### Scenario: Source binding evidence export remains read-only

- **WHEN** source binding evidence is exported or refreshed
- **THEN** it does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG

### Requirement: Source binding review is a provider capability

The system SHALL expose source binding review as a discoverable provider capability while preserving the provider boundary.

#### Scenario: Capability catalog advertises source binding review

- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes capability id `knowledge.provider.source_bindings` with a `GET /api/provider/source-bindings` invocation and `ProviderSourceBindingSummaryResponse` response schema reference

#### Scenario: Provider manifest includes the source binding capability id

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest capability ids include `knowledge.provider.source_bindings`

#### Scenario: Preflight can require source binding review

- **WHEN** a caller requests provider preflight with `knowledge.provider.source_bindings` as a required capability id
- **THEN** the preflight passes required capability and schema reference checks when the endpoint contract is available

#### Scenario: Capability remains read-only evidence

- **WHEN** the provider advertises `knowledge.provider.source_bindings`
- **THEN** the capability description states that source-to-agent binding policy, approvals, audit, and final binding execution remain external control-plane responsibilities

### Requirement: Provider API supports optional component access token

The system SHALL support an optional component-level access token for provider API endpoints without changing successful capability contracts.

#### Scenario: Local provider remains open when token is unset

- **WHEN** `PROVIDER_API_KEY` is not configured
- **THEN** requests to `/api/*` continue to work without access credentials

#### Scenario: API request without token is rejected

- **WHEN** `PROVIDER_API_KEY` is configured and a caller requests `/api/provider/manifest` without credentials
- **THEN** the provider responds with HTTP 401 and a machine-readable provider error code

#### Scenario: API request accepts bearer token

- **WHEN** `PROVIDER_API_KEY` is configured and a caller sends `Authorization: Bearer <token>` with the matching value
- **THEN** the `/api/*` request is allowed to reach the underlying route

#### Scenario: API request accepts provider key header

- **WHEN** `PROVIDER_API_KEY` is configured and a caller sends `X-Provider-Api-Key` with the matching value
- **THEN** the `/api/*` request is allowed to reach the underlying route

#### Scenario: Health remains public

- **WHEN** `PROVIDER_API_KEY` is configured
- **THEN** `GET /health` remains callable without access credentials

#### Scenario: Access guard is not a policy engine

- **WHEN** provider API key protection is enabled
- **THEN** the provider still does not own user identity, roles, approvals, audit policy, or source-to-agent binding decisions

### Requirement: Provider manifest advertises component access metadata

The system SHALL expose machine-readable component access metadata in the provider integration manifest without revealing secret values.

#### Scenario: Manifest identifies public and protected paths

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest access metadata identifies `/health` as public and `/api/*` as protected when provider API key protection is configured

#### Scenario: Manifest lists accepted access headers

- **WHEN** a caller inspects manifest access metadata
- **THEN** it lists `Authorization: Bearer <token>` and `X-Provider-Api-Key: <token>` as accepted component access header schemes

#### Scenario: Manifest redacts secret values

- **WHEN** `PROVIDER_API_KEY` is configured
- **THEN** the manifest reports that a provider API key is configured without including the secret value

#### Scenario: Access metadata preserves provider boundary

- **WHEN** manifest access metadata is exposed
- **THEN** it states that the provider access token is component-level access control and does not represent user identity, RBAC, approvals, audit policy, or source-to-agent binding

### Requirement: Provider includes lightweight container deployment profile

The system SHALL provide a lightweight container deployment profile that can run the provider component without changing runtime capability contracts.

#### Scenario: Container image starts provider API

- **WHEN** the deployment image is built from the provided Dockerfile
- **THEN** it starts `uvicorn app.main:app` on port `8020`

#### Scenario: Compose profile declares component health check

- **WHEN** the compose example is reviewed
- **THEN** it declares a health check against `GET /health`

#### Scenario: Runtime state is mounted, not baked into image

- **WHEN** the container deployment profile is reviewed
- **THEN** source documents, index lifecycle state, and model artifacts are represented as mounted runtime directories rather than copied into the image

#### Scenario: Deployment profile preserves local defaults

- **WHEN** the compose example is used without production overrides
- **THEN** it keeps conservative fixture/mock defaults and does not require Qdrant, BGE-M3 downloads, GraphRAG storage, or external LLM services

#### Scenario: Secrets remain external

- **WHEN** deployment configuration is documented
- **THEN** provider API keys and Qdrant API keys are represented as environment variables and are not committed as concrete secret values

### Requirement: Provider deployed HTTP smoke evidence can be exported

The system SHALL provide a read-only deployed provider smoke probe that validates an already-running provider component over HTTP using a configured base URL and optional provider API credentials.

#### Scenario: Deployed smoke validates public health

- **WHEN** the deployed smoke probe runs against a reachable provider base URL
- **THEN** it requests `GET /health` without provider API credentials and records the provider health status in the exported evidence

#### Scenario: Deployed smoke calls required discovery endpoints

- **WHEN** a caller runs the deployed provider smoke export against a running provider base URL
- **THEN** the probe calls `GET /health`, `GET /api/provider/manifest`, `GET /api/provider/preflight`, `GET /api/provider/source-bindings`, and `GET /api/provider/handoff`

#### Scenario: Deployed smoke supports provider API credentials

- **WHEN** the deployed smoke probe runs with a provider API key
- **THEN** it sends provider API credentials to `GET /api/provider/manifest`, `GET /api/provider/preflight`, `GET /api/provider/source-bindings`, and `GET /api/provider/handoff` without writing the secret value to evidence reports

#### Scenario: Deployed smoke validates source binding review

- **WHEN** the deployed source binding summary endpoint returns `status=ready` or `status=review`
- **THEN** the smoke report marks the source binding check as passing and summarizes source count and bindable source count

#### Scenario: Deployed smoke blocks invalid source binding evidence

- **WHEN** the deployed source binding summary endpoint is unreachable, returns non-200, returns invalid JSON, or reports `status=blocked`
- **THEN** the smoke report marks the source binding check as `blocked` and the overall smoke status as `blocked`

#### Scenario: Deployed smoke writes review artifacts

- **WHEN** the deployed smoke export command completes
- **THEN** it writes machine-readable JSON and human-readable Markdown files with base URL, check status, provider identity, handoff status, and operation notes without writing secret values

#### Scenario: Deployed smoke fails closed

- **WHEN** the provider base URL is unreachable, returns a non-200 discovery response, returns invalid JSON, exposes an incompatible manifest or preflight, reports blocked source binding evidence, or reports blocked handoff evidence
- **THEN** the deployed smoke report marks status `blocked` and the export command exits with a failure status after writing evidence when possible

#### Scenario: Deployed smoke remains read-only

- **WHEN** deployed smoke runs
- **THEN** it does not execute document retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, model downloads, graph queries, provider registration, heartbeat governance, audit policy, source-to-agent binding, or final answer policy

### Requirement: Deployed smoke summarizes source binding actions

The system SHALL include compact source status and recommended action rollups when deployed provider smoke validates live source binding evidence.

#### Scenario: Deployed smoke summarizes source binding statuses

- **WHEN** the deployed provider smoke probe receives source binding summary evidence from `GET /api/provider/source-bindings`
- **THEN** the `provider_source_bindings` check details include counts for source binding row statuses

#### Scenario: Deployed smoke summarizes source binding recommended actions

- **WHEN** the deployed provider smoke probe receives source binding summary evidence from `GET /api/provider/source-bindings`
- **THEN** the `provider_source_bindings` check details include counts for source binding recommended actions

#### Scenario: Deployed smoke source binding action summary remains read-only

- **WHEN** source binding status and action counts are summarized in deployed provider smoke evidence
- **THEN** the probe does not create source-to-agent bindings, create ingestion jobs, rebuild indexes, execute retrieval or answer composition, call embedding models, call vector databases, or execute GraphRAG

### Requirement: Source binding summary exposes compact aggregate counts

The system SHALL include compact aggregate counts in the source binding summary response so external control planes can quickly review binding readiness without recomputing common totals from source rows.

#### Scenario: Source binding response includes aggregate counts

- **WHEN** a caller requests `GET /api/provider/source-bindings`
- **THEN** the response includes `total_source_count`, `bindable_source_count`, `status_counts`, and `recommended_action_counts` derived from the returned source rows

#### Scenario: Source binding aggregate counts remain evidence-only

- **WHEN** the provider builds source binding aggregate counts
- **THEN** it does not create source-to-agent bindings, run approvals, write audit records, create ingestion jobs, rebuild indexes, execute retrieval, compose answers, or execute GraphRAG

#### Scenario: Source binding export includes aggregate counts

- **WHEN** a caller exports source binding evidence
- **THEN** the JSON and Markdown outputs include the compact aggregate counts alongside the detailed source rows

### Requirement: Source binding aggregate counts are reused by evidence summaries

The system SHALL prefer provider-owned source binding aggregate counts when handoff and deployed-smoke evidence summarize source binding readiness.

#### Scenario: Handoff summary reuses source binding aggregate counts

- **WHEN** the provider handoff bundle reads source binding evidence that includes `total_source_count`, `bindable_source_count`, `status_counts`, and `recommended_action_counts`
- **THEN** the `source_binding_summary` artifact summary uses those aggregate values instead of recomputing them from source rows

#### Scenario: Deployed smoke reuses source binding aggregate counts

- **WHEN** the deployed provider smoke probe reads a source binding response that includes aggregate count fields
- **THEN** the `provider_source_bindings` check details use those aggregate values

#### Scenario: Older source binding evidence remains compatible

- **WHEN** handoff or deployed-smoke source binding evidence does not include aggregate count fields
- **THEN** the system falls back to deriving counts from returned source rows

#### Scenario: Aggregate count reuse remains read-only

- **WHEN** source binding aggregate counts are reused by evidence summaries
- **THEN** the system does not create source-to-agent bindings, run approvals, write audit records, create ingestion jobs, rebuild indexes, execute retrieval, compose answers, or execute GraphRAG

### Requirement: Provider handoff includes compact Phase 3 retrieval baseline evidence

The system SHALL include optional Phase 3 retrieval evidence rows in provider handoff so external reviewers can inspect benchmark quality signals without opening multiple files separately.

#### Scenario: Handoff summarizes Phase 3 FP/FN review evidence

- **WHEN** provider handoff reads the local FP/FN review artifact
- **THEN** it summarizes `false_positive_count`, `false_negative_count`, `false_positive_rate`, and `false_negative_rate`

#### Scenario: Missing FP/FN review evidence remains non-blocking

- **WHEN** the optional FP/FN review artifact is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

### Requirement: Provider handoff includes compact Phase 3 readiness export evidence

The system SHALL include optional Phase 3 retrieval promotion readiness evidence in provider handoff so reviewers can inspect the current promotion gap picture without opening the export files separately.

#### Scenario: Handoff summarizes readiness export

- **WHEN** provider handoff reads the Phase 3 readiness export
- **THEN** it summarizes the report status, decision, and open gates in a compact row

#### Scenario: Missing readiness export remains non-blocking

- **WHEN** the optional Phase 3 readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

### Requirement: Provider publishes evidence pack consumption contract
The system SHALL maintain a read-only local evidence pack consumption contract artifact that explains the stable `evidence_pack-v1` fields, caller rules, and fail-closed behavior.

#### Scenario: Contract artifact is discoverable
- **WHEN** the Phase 4 evidence pack consumption contract is reviewed
- **THEN** it points at the local contract document under `docs/benchmark/chinese-seed/evidence-pack-consumption-contract/`

#### Scenario: Contract artifact stays local and read-only
- **WHEN** the contract document is published or refreshed
- **THEN** it remains a local review artifact and does not change runtime retrieval defaults, final answer policy, or provider HTTP contracts

#### Scenario: Contract artifact describes caller ownership
- **WHEN** the contract document is reviewed
- **THEN** it explains that `allowed_citations` is the caller allowlist, `insufficient_evidence` is a valid fail-closed envelope, and diagnostic fields remain diagnostic

### Requirement: Provider handoff includes compact Phase 4 evidence pack readiness export evidence

The system SHALL include optional Phase 4 evidence pack readiness export evidence in provider handoff so reviewers can inspect the current evidence-pack contract coverage without opening the export files separately.

#### Scenario: Handoff summarizes readiness export

- **WHEN** provider handoff reads the Phase 4 readiness export
- **THEN** it summarizes the report status, decision, and contract coverage in a compact row

#### Scenario: Missing readiness export remains non-blocking

- **WHEN** the optional Phase 4 readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

### Requirement: Provider handoff includes compact Phase 4 caller-consumption smoke evidence

The system SHALL include optional Phase 4 caller-consumption smoke evidence in provider handoff so reviewers can inspect the caller-facing evidence-pack contract coverage without opening the smoke files separately.

#### Scenario: Handoff summarizes caller-consumption smoke

- **WHEN** provider handoff reads the Phase 4 caller-consumption smoke
- **THEN** it summarizes the report status, key checks, and caller allowlist/fail-closed coverage in a compact row

#### Scenario: Missing caller-consumption smoke remains non-blocking

- **WHEN** the optional caller-consumption smoke is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

### Requirement: Provider handoff includes compact Phase 5 graph use-case readiness export evidence

The system SHALL include optional Phase 5 graph use-case readiness export evidence in provider handoff so reviewers can inspect the current GraphRAG boundary without opening the export files separately.

#### Scenario: Handoff summarizes graph readiness export

- **WHEN** provider handoff reads the Phase 5 graph readiness export
- **THEN** it summarizes the report status, decision, and graph boundary evidence in a compact row

#### Scenario: Missing graph readiness export remains non-blocking

- **WHEN** the optional Phase 5 graph readiness export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

### Requirement: Provider handoff includes compact Phase 5 graph boundary smoke summary evidence

The system SHALL include optional Phase 5 graph boundary smoke summary evidence in provider handoff so reviewers can inspect the current GraphRAG boundary without opening the full provider contract smoke report separately.

#### Scenario: Handoff summarizes graph boundary smoke

- **WHEN** provider handoff reads the Phase 5 graph boundary smoke summary
- **THEN** it summarizes graph schema discovery, the planned graph query boundary, and the compact graph boundary evidence in one row

#### Scenario: Missing graph boundary smoke summary remains non-blocking

- **WHEN** the optional Phase 5 graph boundary smoke summary is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

### Requirement: Provider handoff can summarize optional Phase 3 runtime diagnostics evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 candidate runtime diagnostics evidence as read-only review context.

#### Scenario: Handoff summarizes runtime diagnostics

- **WHEN** provider handoff reads the Phase 3 candidate runtime diagnostics export
- **THEN** it summarizes report status, decision, and prerequisite-check coverage in a compact optional row

#### Scenario: Missing runtime diagnostics remains non-blocking

- **WHEN** the optional Phase 3 candidate runtime diagnostics export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates runtime diagnostics before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates the Phase 3 candidate runtime diagnostics export before final handoff bundle generation

### Requirement: Provider handoff can summarize optional Phase 3 cross-case FP/FN smoke evidence

The system SHALL allow provider handoff bundle and handoff refresh workflows to include optional Phase 3 hybrid cross-case FP/FN smoke evidence as read-only review context.

#### Scenario: Handoff summarizes cross-case smoke

- **WHEN** provider handoff reads the Phase 3 hybrid cross-case FP/FN smoke export
- **THEN** it summarizes smoke status and cross-case check coverage in a compact optional row

#### Scenario: Missing cross-case smoke remains non-blocking

- **WHEN** the optional cross-case smoke export is missing
- **THEN** handoff marks it reviewable and preserves existing required-artifact blocking behavior

#### Scenario: Refresh regenerates cross-case smoke before handoff

- **WHEN** provider handoff refresh runs
- **THEN** it regenerates Phase 3 hybrid cross-case FP/FN smoke evidence before final handoff bundle generation

