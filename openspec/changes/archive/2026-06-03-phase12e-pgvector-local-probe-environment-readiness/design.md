## Context

Phase 12d proved that the live probe can describe its own blocker. Phase 12e shifts one layer earlier and makes the local environment explicit so the probe is no longer blocked by invisible setup assumptions.

The repository still keeps this slice lightweight. The environment package is optional, local-first, and read-only. It does not write business data or change runtime defaults. Its job is to make the pgvector probe reproducible when a developer wants to run it.

## Goals / Non-Goals

**Goals:**
- Create a pgvector local probe environment slice that is clearly distinct from the live probe report.
- Keep the environment package optional and local.
- Make the local environment visible in handoff and refresh evidence without changing runtime defaults.
- Preserve the provider-first boundary and keep caller ownership, GraphRAG execution, and parser expansion out of scope.

**Non-Goals:**
- No default backend promotion.
- No hard PostgreSQL dependency in the main application requirements.
- No ingestion, indexing, or vector database writes from the provider.
- No caller control-plane changes, identity policy changes, or answer policy changes.
- No GraphRAG execution enablement.

## Decisions

1. **Use an optional environment package instead of a mandatory runtime dependency**
   - Rationale: the pgvector probe should remain opt-in and developer-owned.
   - Alternatives considered:
     - Add psycopg to the main requirements. Rejected because it would make every environment carry a dependency that only a subset of users needs.

2. **Keep the local environment read-only from the provider perspective**
   - Rationale: the environment should enable a probe, not mutate provider behavior.
   - Alternatives considered:
     - Move probe setup into application startup. Rejected because it would couple candidate evaluation to the provider runtime.

3. **Reuse the same handoff/refresh evidence flow**
   - Rationale: review artifacts should remain discoverable through the same local bundle and refresh lane.
   - Alternatives considered:
     - Standalone report outside handoff. Rejected because it would fragment the review path.

4. **Keep the same reversible decision vocabulary**
   - Rationale: `keep_current_default`, `continue_spike`, and `eligible_for_promotion_review` already match the candidate-evaluation language used elsewhere.
   - Alternatives considered:
     - Introduce an environment-specific decision taxonomy. Rejected because it would make review harder to compare across phases.

## Risks / Trade-offs

- [Risk] The environment package may be ignored and the live probe will stay blocked.
  [Mitigation] Make the runbook and exported evidence point to the exact files needed to unblock Phase 12d.
- [Risk] The new phase could be mistaken for runtime promotion.
  [Mitigation] Keep the report and docs explicit that this is evidence-only and does not change defaults.
- [Risk] The environment package could drift from the live probe report.
  [Mitigation] Keep the local environment report and Phase 12d report in the same handoff chain.

## Migration Plan

1. Add the pgvector local environment spec and design.
2. Implement the optional dependency, compose profile, init SQL, and runbook.
3. Wire the artifact into handoff and refresh as optional evidence.
4. Validate with focused tests and strict OpenSpec checks.
5. Archive the change after the review pass is complete.

Rollback is simple: remove the optional artifact wiring and leave the provider defaults unchanged. Because this phase does not alter runtime behavior, rollback does not require data migration.
