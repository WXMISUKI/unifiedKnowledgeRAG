## Context

The repository already exposes `evidence_pack-v1` on RAG retrieve and answer envelopes, and the provider contract smoke already checks the key fail-closed and provenance semantics. The missing piece is a stable readiness export that can be regenerated, compared, and surfaced in handoff without introducing new runtime behavior.

The export should behave like a local evidence reporter, not a policy engine. It should consolidate the current contract document and smoke evidence into one compact artifact while keeping caller ownership intact.

## Goals / Non-Goals

**Goals:**

- Export a single Phase 4 readiness report in JSON and Markdown.
- Make the report usable from handoff and refresh workflows.
- Keep the report deterministic, local, and read-only.

**Non-Goals:**

- Changing `evidence_pack-v1` semantics or caller ownership.
- Adding new runtime APIs, background jobs, or prompt policy.
- Replacing the caller consumption contract document; the export should complement it.

## Decisions

- Use one readiness report object with a small summary table.
  That keeps handoff summaries compact and easy to keep current.

- Derive readiness from the existing local contract doc and provider contract smoke evidence.
  The export should summarize current evidence, not rerun business logic or invent new policy.

- Keep the export source paths explicit.
  Every row should point back to the underlying local evidence artifact so reviewers can drill in quickly.

## Risks / Trade-offs

- The export can drift from the contract doc if one is updated without the other.
  Mitigation: keep the report aligned with the existing `evidence_pack-v1` semantics and refresh both from the same evidence chain.

- Integrating the export into handoff can widen the bundle slightly.
  Mitigation: make it optional and keep the summary compact.
