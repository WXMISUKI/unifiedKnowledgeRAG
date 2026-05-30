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

#### Scenario: Smoke evidence can be exported
- **WHEN** a caller runs the provider contract smoke export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files without changing provider HTTP API contracts

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
