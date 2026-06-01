## Context

The provider already exposes graph schemas and keeps graph query execution planned. Provider contract smoke already proves both the graph schema discovery and the planned boundary, but reviewers still have to sift those checks out of the larger contract report. A dedicated smoke summary can consolidate just the graph boundary evidence into a compact local artifact.

## Goals / Non-Goals

**Goals:**

- Export a single Phase 5 graph boundary smoke summary in JSON and Markdown.
- Make the summary usable from handoff and refresh workflows.
- Keep the summary deterministic, local, and read-only.

**Non-Goals:**

- Implementing GraphRAG execution.
- Adding Neo4j, entity extraction, ontology workflows, or graph-store dependencies.
- Promoting graph query execution or graph storage by default.

## Decisions

- Derive the smoke summary from the existing provider contract smoke evidence and graph schema discovery details.
  The summary should consolidate current evidence, not rerun business logic or invent new policy.

- Keep the output small and review-friendly.
  The smoke summary should be a compact artifact that is easy to include in handoff without replacing the full provider contract smoke report.

- Keep the export source paths explicit.
  Every row should point back to the underlying local evidence artifact so reviewers can drill in quickly.

## Risks / Trade-offs

- The summary can drift from the contract smoke if one is updated without the other.
  Mitigation: keep the summary aligned with the existing graph boundary evidence and refresh both from the same evidence chain.

- Integrating the summary into handoff can widen the bundle slightly.
  Mitigation: make it optional and keep the summary compact.
