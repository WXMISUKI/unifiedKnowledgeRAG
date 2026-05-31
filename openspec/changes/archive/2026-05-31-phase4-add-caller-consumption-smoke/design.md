## Context

The repository already exposes `evidence_pack-v1` on successful RAG envelopes, and the caller consumption contract explains how callers should interpret `answerable` versus `insufficient_evidence`. The missing piece is a compact executable smoke that checks the caller-facing rules directly against the shared evidence-pack builder.

The smoke should behave like a local contract verifier. It should prove that a caller can treat `allowed_citations` as the only allowlist in the answerable case and can fail closed when no evidence is returned, without pulling in a new runtime path.

## Goals / Non-Goals

**Goals:**

- Export a single Phase 4 caller-consumption smoke report in JSON and Markdown.
- Prove the answerable and insufficient-evidence branches using the shared evidence-pack helper.
- Keep the report deterministic, local, and read-only.

**Non-Goals:**

- Changing `evidence_pack-v1` semantics or caller ownership.
- Adding new runtime APIs, background jobs, or HTTP smoke endpoints.
- Replacing the provider contract smoke; the new smoke complements it from the caller-consumption angle.

## Decisions

- Use the shared `build_evidence_pack` helper directly.
  That keeps the smoke focused on caller semantics instead of duplicating provider HTTP coverage.

- Cover exactly the two critical caller branches.
  One answerable sample proves the allowlist and provenance path; one empty sample proves the fail-closed path.

- Keep the export source paths explicit.
  The report should point back to the contract doc and the local evidence-pack helper inputs so reviewers can drill in quickly.

## Risks / Trade-offs

- This smoke overlaps a little with unit tests and provider contract smoke.
  Mitigation: keep the checks focused on caller-facing branching and exported evidence, not on the provider runtime itself.

- Using synthetic documents means the smoke is still local evidence, not a customer-corpus benchmark.
  Mitigation: treat it as a minimal contract smoke only; customer-like corpus work remains separate.
