## Context

`GET /api/graph/schemas` already exposes graph namespace metadata, and `knowledge.graph.query` is advertised as a planned capability. Provider preflight currently checks that the graph capability boundary exists, but it does not summarize the available graph schemas. This makes the provider look less ready than it is for lightweight integration review, while still intentionally not ready for graph execution.

## Goals / Non-Goals

**Goals:**

- Add graph namespace discovery details to the existing `graph_boundary` preflight check.
- Keep graph execution status explicit as `planned`.
- Preserve the current behavior where planned graph capability passes provider preflight.
- Avoid any new graph runtime dependency or graph query execution.

**Non-Goals:**

- Implementing `/api/graph/query` execution.
- Adding Neo4j, graph stores, entity extraction, ontology workflows, graph indexing, or GraphRAG retrieval.
- Changing graph schema endpoint response models.
- Changing provider binding requirements or runtime defaults.

## Decisions

- Reuse `list_graphs()` from the source catalog inside preflight.
  - Rationale: The source catalog already owns graph namespace metadata, and reading it is side-effect free.
  - Alternative considered: Call the graph router or construct a graph service. That would be heavier and less direct.

- Add compact lists/counts in `graph_boundary.details`.
  - Rationale: Preflight details are already a machine-readable diagnostic surface for external control planes.
  - Alternative considered: Add a new endpoint. Existing `/api/graph/schemas` already handles full schema discovery, so a new endpoint would duplicate responsibility.

## Risks / Trade-offs

- Preflight details become slightly larger. Mitigation: include only ids, statuses, store labels, and count.
- Callers might mistake discoverable graph schemas for executable GraphRAG. Mitigation: keep `execution_status=planned` and include an explicit boundary note.
