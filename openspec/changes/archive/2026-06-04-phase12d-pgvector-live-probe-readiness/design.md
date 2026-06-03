## Context

Phase 12c proved that pgvector can be tracked as a candidate without changing runtime defaults. Phase 12d moves one step further by making the probe itself evidence-backed: if a local PostgreSQL instance is configured and a driver is available, the provider can verify connection and minimal pgvector runtime posture without writing data.

The repository still keeps this slice lightweight. The live probe remains optional, read-only, and local-first. If the environment is not ready, the report stays reviewable instead of pretending the backend is promoted.

## Goals / Non-Goals

**Goals:**
- Create a pgvector live probe slice that is clearly distinct from the configuration-only Phase 12c report.
- Keep the probe read-only and local.
- Make the probe visible in handoff and refresh evidence without changing runtime defaults.
- Preserve the provider-first boundary and keep caller ownership, GraphRAG execution, and parser expansion out of scope.

**Non-Goals:**
- No default backend promotion.
- No new hard PostgreSQL dependency in this change.
- No ingestion, indexing, or vector database writes.
- No caller control-plane changes, identity policy changes, or answer policy changes.
- No GraphRAG execution enablement.

## Decisions

1. **Use an optional driver-backed probe instead of a mocked readiness claim**
   - Rationale: the next useful evaluation step is to verify whether a real local PostgreSQL + pgvector instance can answer the expected minimal probe.
   - Alternatives considered:
     - Keep the phase configuration-only. Rejected because Phase 12c already covers that shape.
     - Add a hard dependency and force the probe on every environment. Rejected because it would make the slice heavier than the current evidence justifies.

2. **Keep the live probe read-only**
   - Rationale: the probe should verify existing infrastructure posture, not mutate it.
   - Alternatives considered:
     - Create tables or indexes during the probe. Rejected because that would cross into setup/migration behavior.

3. **Reuse the same handoff/refresh evidence flow**
   - Rationale: review artifacts should remain discoverable through the same local bundle and refresh lane.
   - Alternatives considered:
     - Standalone report outside handoff. Rejected because it would fragment the review path.

4. **Keep the same reversible decision vocabulary**
   - Rationale: `keep_current_default`, `continue_spike`, and `eligible_for_promotion_review` already match the candidate-evaluation language used elsewhere.
   - Alternatives considered:
     - Introduce a probe-specific decision taxonomy. Rejected because it would make review harder to compare across phases.

## Risks / Trade-offs

- [Risk] The probe may still be blocked on machines without PostgreSQL or the `psycopg` driver.
  [Mitigation] The report stays reviewable and the handoff refresh maps blocked probe status to a non-fatal refresh step status.
- [Risk] The new phase could be mistaken for a runtime promotion.
  [Mitigation] Keep the report and docs explicit that this is evidence-only and does not change defaults.
- [Risk] The probe may be overinterpreted as a full migration plan.
  [Mitigation] Limit the probe to minimal connectivity and schema/posture checks only.

## Migration Plan

1. Add the pgvector live probe spec and design.
2. Implement the read-only probe export and optional driver path.
3. Wire the artifact into handoff and refresh as optional evidence.
4. Validate with focused tests and strict OpenSpec checks.
5. Archive the change after the review pass is complete.

Rollback is simple: remove the optional artifact wiring and leave the provider defaults unchanged. Because this phase does not alter runtime behavior, rollback does not require data migration.
