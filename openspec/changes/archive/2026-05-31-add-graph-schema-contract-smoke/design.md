## Context

`GET /api/graph/schemas` is the lightweight graph discovery surface. `POST /api/graph/query` intentionally returns a structured `GRAPH_NOT_IMPLEMENTED` error in this slice. Contract smoke currently validates the planned query boundary, but it does not prove that graph schema metadata is discoverable.

## Goals / Non-Goals

**Goals:**

- Validate `GET /api/graph/schemas` in provider contract smoke.
- Keep graph schema discovery separate from graph query execution.
- Include compact graph namespace details in smoke evidence.
- Preserve all current provider behavior and runtime defaults.

**Non-Goals:**

- Implementing graph query execution.
- Adding Neo4j, graph stores, entity extraction, ontology workflow, graph indexing, or GraphRAG retrieval.
- Adding live deployed HTTP calls beyond existing local contract smoke.

## Decisions

- Add a new contract smoke check named `graph_schema_discovery`.
  - Rationale: Schema discovery and query execution are different contracts. Separate checks make the boundary clear and reviewable.
  - Alternative considered: Fold schema discovery into `graph_planned_boundary`. That would hide a useful readiness signal inside an error-boundary check.

- Keep the check read-only and local.
  - Rationale: Contract smoke is a local integration artifact and should not require external graph infrastructure.
  - Alternative considered: Probe a real graph store. That would violate the roadmap gate for GraphRAG execution.

## Risks / Trade-offs

- The contract smoke check count changes from 8 to 9. Mitigation: update focused tests and smoke evidence expectations.
- Graph schema details are only lightweight metadata. Mitigation: execution remains covered by the planned boundary check and future GraphRAG work requires separate evidence.
