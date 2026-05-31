## Context

The provider already exports source binding evidence and includes it in the provider handoff bundle. The current handoff artifact row for `source_binding_summary` reports the source-binding report status and bindable source count, which is useful but not enough for a deployment reviewer to quickly understand the action profile when some sources require review or are blocked.

This change stays inside the existing file-backed handoff bundle. It advances Phase 2/6 evidence review without adding runtime orchestration, parser support, indexing execution, retrieval execution, answer composition, or GraphRAG behavior.

## Goals / Non-Goals

**Goals:**

- Summarize source binding evidence in the handoff bundle with counts by source status.
- Summarize source binding recommended actions in the same artifact row.
- Preserve existing handoff status semantics and read-only behavior.
- Keep the persisted source binding report shape unchanged.

**Non-Goals:**

- Creating source-to-agent bindings.
- Changing binding decisions, preflight behavior, ingestion behavior, or retrieval defaults.
- Regenerating source binding evidence from the handoff endpoint.
- Adding parser, vector-store, reranker, answer-composer, or GraphRAG dependencies.

## Decisions

- Extend only the handoff bundle source-binding artifact summary.
  - Rationale: The full source binding report already contains row-level statuses and recommended actions. The handoff bundle only needs a compact rollup, not duplicated row payloads.
  - Alternative considered: Add a new artifact type or nested summary field. That would make the evidence model heavier and is unnecessary for current reviewers.

- Use deterministic count maps for `sources[].status` and `sources[].recommended_action`.
  - Rationale: Count maps are compact, stable, machine-readable inside the summary string, and cheap to compute from the existing JSON evidence.
  - Alternative considered: Include every source id and reason in the handoff summary. That duplicates the detailed report and can make the handoff table noisy.

- Preserve fail-closed status handling.
  - Rationale: If source binding evidence reports `blocked`, the handoff bundle should remain blocked exactly as it does today.
  - Alternative considered: Treat source binding as review-only. That would weaken the existing requirement that source binding evidence participates in handoff readiness.

## Risks / Trade-offs

- Summary strings can become longer when many recommended actions exist. Mitigation: report action counts instead of per-source details.
- Existing consumers that compare the exact summary string may need to accept the enriched summary. Mitigation: endpoint paths, artifact ids, status fields, and recommended actions remain unchanged.
