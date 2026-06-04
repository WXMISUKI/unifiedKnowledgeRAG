## Context

Phase 12e made the optional local pgvector environment explicit. Phase 12d still represents the live probe itself, but the repo does not yet have a dedicated slice that captures the local rerun path for that probe and makes the execution boundary visible in handoff evidence.

This change stays lightweight. It packages execution-readiness evidence and a rerun runbook; it does not attempt to benchmark retrieval quality, ingest business data, or alter provider defaults.

## Goals / Non-Goals

**Goals:**
- Create a Phase 12f execution-readiness slice for rerunning the local pgvector live probe.
- Keep the execution path optional, local-first, and read-only from the provider perspective.
- Make the rerun path visible in handoff and refresh evidence without changing runtime defaults.
- Preserve the provider-first boundary and keep caller ownership, GraphRAG execution, and parser expansion out of scope.

**Non-Goals:**
- No default backend promotion.
- No hard PostgreSQL dependency in the main application requirements.
- No ingestion, indexing, or vector database writes from the provider.
- No caller control-plane changes, identity policy changes, or answer policy changes.
- No GraphRAG execution enablement.

## Decisions

1. **Use a local execution-readiness artifact instead of folding the rerun path into Phase 12e**
   - Rationale: Phase 12e is about the environment package itself; Phase 12f should capture the operator step that actually reruns the live probe.
   - Alternatives considered:
     - Extend Phase 12e with execution semantics. Rejected because it blurs the boundary between environment packaging and probe execution.

2. **Keep the rerun path read-only and optional**
   - Rationale: the provider should expose evidence and guidance, not own PostgreSQL governance or automatic execution policy.
   - Alternatives considered:
     - Run the probe automatically from the provider. Rejected because it would couple candidate evaluation to runtime behavior.

3. **Reuse the same handoff/refresh evidence flow**
   - Rationale: review artifacts should remain discoverable through the same bundle and refresh lane already used by Phase 12b through 12e.
   - Alternatives considered:
     - Standalone report outside handoff. Rejected because it would fragment the review path.

4. **Keep the same reversible decision vocabulary**
   - Rationale: `keep_current_default`, `continue_spike`, and `eligible_for_promotion_review` already match the candidate-evaluation language used elsewhere.
   - Alternatives considered:
     - Introduce a new execution-specific taxonomy. Rejected because it would make review harder to compare across phases.

## Risks / Trade-offs

- [Risk] The rerun path may be mistaken for runtime promotion.
  - Mitigation: keep the report and docs explicit that this is execution-readiness evidence only and does not change defaults.
- [Risk] The live probe can still stay blocked if the local environment is not actually started.
  - Mitigation: keep the report honest about current Phase 12d status and surface the exact next step in the runbook.
- [Risk] The new phase could drift from the environment package.
  - Mitigation: anchor it to the Phase 12e report and keep both artifacts in the same handoff chain.

## Migration Plan

1. Add the Phase 12f execution-readiness spec and design.
2. Implement the local execution report, runbook, and export helper.
3. Wire the artifact into handoff and refresh as optional evidence.
4. Validate with focused tests and strict OpenSpec checks.
5. Archive the change after the review pass is complete.

Rollback is simple: remove the optional artifact wiring and leave the provider defaults unchanged. Because this phase does not alter runtime behavior, rollback does not require data migration.
