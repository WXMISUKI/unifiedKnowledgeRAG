## Context

Phase 3 promotion review is still evidence-gated. We already have baseline benchmark evidence, runtime diagnostics, and deployment readiness, but the latency shape of the local seed run is not surfaced as a first-class artifact. Reviewers benefit from seeing that latency profile next to the resource posture that produced it.

## Goals / Non-Goals

**Goals**

- Export a compact local Phase 3 latency/resource diagnostics report.
- Surface local benchmark latency statistics alongside resource/deployment posture.
- Keep the artifact deterministic, local, and easy to refresh.

**Non-Goals**

- Changing retrieval runtime defaults.
- Introducing new retrieval backends, rerankers, or GraphRAG execution.
- Modifying provider HTTP contracts or control-plane responsibilities.
- Treating local latency evidence as a promotion decision by itself.

## Decisions

- Use the current Chinese-seed benchmark evidence as the latency source of truth.
- Pair the benchmark latency profile with the current deployment readiness and runtime diagnostics snapshots so reviewers can see both performance shape and resource posture together.
- Keep the report read-only and local; no new live API, no new remote dependency, and no automatic promotion logic.

## Risks / Trade-offs

- Latency values are local and environment-sensitive, so the report must be read as review evidence rather than a production SLO claim.
- The report will depend on the current benchmark evidence being refreshed first; that is acceptable because it is part of the existing evidence chain.
