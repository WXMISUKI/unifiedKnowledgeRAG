## Context

`GET /api/provider/source-bindings` already returns per-source binding readiness rows. MyPrivateAgent or another caller can derive aggregate readiness from those rows, but every caller would need to duplicate the same filtering and counting logic.

The provider boundary remains data-plane evidence only. This change should make the existing evidence easier to consume without introducing binding execution, source-to-agent policy, ingestion, retrieval, or GraphRAG behavior.

## Goals / Non-Goals

**Goals:**

- Add deterministic compact aggregate counts to the source binding response.
- Reuse the existing source rows as the single source of truth.
- Surface the same counts in exported JSON/Markdown evidence.
- Keep the change backwards-compatible for existing source row consumers.

**Non-Goals:**

- Creating or storing source-to-agent bindings.
- Adding identity, authorization policy, approvals, audit, or registration workflows.
- Running ingestion, retrieval, answer composition, vector stores, or GraphRAG.
- Adding parser dependencies or changing source readiness rules.

## Decisions

- Add top-level counts instead of a new endpoint.
  The existing source binding endpoint is already the caller-facing evidence surface. A new endpoint would add integration surface area without new capability.

- Compute counts after rows are built.
  The row list already captures source status, bindability, and recommended action. Counting from rows avoids duplicating binding decision logic.

- Keep count keys as dictionaries.
  `status_counts` and `recommended_action_counts` can evolve with existing status/action strings without schema churn.

- Render a short Markdown summary before the detailed source table.
  Reviewers get an immediate readiness overview while preserving row-level diagnostics.

## Risks / Trade-offs

- Response shape grows slightly -> keep additions top-level and compact.
- Counts can be misread as policy decisions -> operation notes and specs keep binding policy caller-owned.
- Future action strings can appear in count dictionaries -> this is acceptable because rows already expose the same strings.
