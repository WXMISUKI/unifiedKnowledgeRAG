## Context

The repository already exposes graph boundary evidence in provider preflight and provider contract smoke, and the roadmap already says GraphRAG must remain use-case driven. The missing piece is a stable readiness export that can be regenerated, compared, and surfaced in handoff without introducing graph execution.

The export should act like a local evidence reporter, not a policy engine. It should consolidate the current graph use-case contract, graph boundary metadata, and planned query boundary into one compact artifact while keeping runtime ownership intact.

## Goals / Non-Goals

**Goals:**

- Export a single Phase 5 readiness report in JSON and Markdown.
- Make the report usable from handoff and refresh workflows.
- Keep the report deterministic, local, and read-only.

**Non-Goals:**

- Implementing GraphRAG execution.
- Adding Neo4j, entity extraction, ontology workflows, or graph-store dependencies.
- Promoting graph query execution or graph storage by default.

## Decisions

- Use one readiness report object with a compact summary table.
  That keeps handoff summaries readable and easy to keep current.

- Derive readiness from the existing graph contract doc and provider contract smoke evidence.
  The export should summarize current evidence, not rerun business logic or invent new policy.

- Keep the export source paths explicit.
  Every row should point back to the underlying local evidence artifact so reviewers can drill in quickly.

## Risks / Trade-offs

- The export can drift from the graph contract if one is updated without the other.
  Mitigation: keep the report aligned with the existing graph boundary evidence and refresh both from the same evidence chain.

- Integrating the export into handoff can widen the bundle slightly.
  Mitigation: make it optional and keep the summary compact.
