# Provider Integration Probe Report

- Status: `bindable`
- Provider: `unifiedKnowledgeProvider`
- Provider Name: `unifiedKnowledgeRAG`
- Contract Version: `knowledge-provider-contract-v1`
- Manifest Version: `provider-integration-manifest-v1`
- Requested Contract Version: `knowledge-provider-contract-v1`
- Requested Capabilities: `knowledge.rag.source_documents, knowledge.rag.retrieve, knowledge.rag.answer, knowledge.graph.query`

## Capability Bindings

| Capability | Status | Path | Example Request |
|---|---|---|---|
| `knowledge.rag.source_documents` | `ready` | `/api/rag/sources/{source_id}/documents` | `present` |
| `knowledge.rag.retrieve` | `ready` | `/api/rag/retrieve` | `present` |
| `knowledge.rag.answer` | `ready` | `/api/rag/answer` | `present` |
| `knowledge.graph.query` | `planned` | `/api/graph/query` | `present` |

## Preflight Checks

| Check | Status | Passed | Reason |
|---|---|---|---|
| `manifest_identity` | `ready` | `True` | `` |
| `contract_version` | `ready` | `True` | `` |
| `health_readiness` | `ok` | `True` | `` |
| `required_capabilities` | `ready` | `True` | `` |
| `schema_references` | `ready` | `True` | `` |
| `graph_boundary` | `planned` | `True` | `` |
