## Context

The local business corpus trial now produces a `go` result for `company_profile_2025_trial`, but it intentionally remains pre-registration. A caller needs a compact package that says what can be reviewed, what is not yet formal, and what the next safe action is.

The handoff should be derived from existing local trial artifacts instead of rerunning extraction or retrieval.

## Goals / Non-Goals

**Goals:**

- Read an existing `local-business-corpus-trial.json`.
- Export a caller-facing JSON/Markdown handoff.
- Preserve `ready_for_caller_review`, `review`, and `blocked` semantics.
- Include paths to markdown, overlay, chunks, and trial report.
- Make non-goals machine-readable for callers.

**Non-Goals:**

- Do not register the source in `source_catalog.py`.
- Do not expose the source through provider HTTP APIs.
- Do not create source bindings or ingestion jobs.
- Do not run MyPrivateAgent, OCR, Qdrant, BGE-M3, pgvector, or GraphRAG.

## Decisions

- Use the trial report as the handoff input.
  - Rationale: the trial report is already the artifact that proved local corpus usability.

- Treat `decision=go` as `ready_for_caller_review`, not `ready_for_production`.
  - Rationale: the source is still local/private and not formally registered.

- Fail closed when required artifact paths are missing from the report.
  - Rationale: a caller handoff without artifact pointers is not actionable.

## Risks / Trade-offs

- The handoff may feel like another evidence artifact -> keep it caller-facing and avoid adding broader readiness chains.
- Paths are local machine paths -> acceptable for local review; remote deployment remains out of scope.
- The handoff does not run HTTP retrieval -> acceptable because the trial already validated local corpus evidence.
