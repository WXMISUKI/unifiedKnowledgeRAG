## Context

The repository already has separate benchmark and review files for Qdrant, BGE-M3, hybrid retrieval, aggregation, relation-aware grading, and FP/FN review. The missing piece is a stable readiness export that synthesizes those gates into one machine-readable report.

The export should feel like a report generator, not a policy engine. It should make the current promotion gaps obvious and keep the runtime boundary intact.

## Goals / Non-Goals

**Goals:**

- Export a single Phase 3 readiness report in JSON and Markdown.
- Make the report usable from handoff and refresh workflows.
- Keep the report deterministic and local.

**Non-Goals:**

- Promoting Qdrant, BGE-M3, hybrid retrieval, aggregation, or relation-aware grading to runtime defaults.
- Creating new runtime APIs or background jobs.
- Replacing the gap matrix doc; the export should complement it.

## Decisions

- Use one readiness report object with a small gate table.
  That makes handoff summaries compact and easy to keep current.

- Treat missing or weak evidence as review, not failure.
  The report exists to expose what still needs work, not to block local development.

- Keep the export source paths explicit.
  Every row should point back to the underlying local evidence artifact so reviewers can drill in quickly.

## Risks / Trade-offs

- The export can drift from the documented gap matrix if the two are updated independently.
  Mitigation: keep the row set aligned and refresh both from the same phase 3 evidence chain.

- Integrating the export into handoff can widen the bundle slightly.
  Mitigation: make it optional and keep the summary compact.
