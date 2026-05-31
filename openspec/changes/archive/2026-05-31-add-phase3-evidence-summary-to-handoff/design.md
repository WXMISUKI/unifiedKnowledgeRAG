## Context

The handoff bundle already consolidates integration, contract, source-binding, and operations evidence. Phase 3 retrieval quality baseline evidence exists under `docs/benchmark/chinese-seed`, but reviewers must manually cross-open it.

This slice should keep handoff lightweight by adding only a compact summary reference, not new benchmark execution logic.

## Goals / Non-Goals

**Goals:**

- Expose a compact Phase 3 baseline evidence summary in handoff.
- Keep the new artifact optional and non-blocking.
- Preserve backward compatibility with older workspaces missing this evidence file.

**Non-Goals:**

- Running benchmark export from handoff.
- Changing retrieval defaults or promotion status.
- Modifying provider HTTP routes or request/response contracts.

## Decisions

- Add a new optional `HandoffEvidenceSpec` entry pointing to
  `docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json`.
- Parse summary metrics from `payload.report.summary`.
- Normalize status to `ready/review/blocked` using existing artifact conventions.

## Risks / Trade-offs

- Evidence schema drift could break parsing -> fallback to `review` with a generic summary.
- More rows in handoff table -> acceptable because it improves one-stop review ergonomics.
