## Why

The provider now exports several useful evidence artifacts for external control planes and operators: integration probe, contract smoke, deployment readiness, and reindex readiness. They are currently discoverable through documentation, but a caller or deployment reviewer still has to know each file path and interpret each report separately.

This change adds a lightweight local handoff bundle that summarizes those existing evidence artifacts into one machine-readable and reviewable package. It advances roadmap Phase 6 without adding platform governance, worker infrastructure, runtime retrieval behavior, or GraphRAG execution.

## What Changes

- Add a local provider handoff bundle report that summarizes the current integration and operations evidence artifacts.
- Include provider identity, contract version, required artifact paths, artifact presence, artifact status, and recommended next action.
- Export JSON and Markdown under `docs/integration/provider-handoff/`.
- Keep the bundle read-only and side-effect free.

## Impact

- Affected specs:
  - `knowledge-provider`: provider handoff evidence can be exported for external control-plane integration.
  - `provider-roadmap`: handoff evidence is Phase 6 operations/integration evidence without expanding provider scope.
- Affected code:
  - New handoff bundle service and export CLI.
- Affected docs/evidence:
  - README, lightweight roadmap, generated handoff bundle JSON/Markdown.

## Non-Goals

- No new HTTP endpoint.
- No provider registration or heartbeat governance.
- No ingestion, reindex execution, embedding/model download, vector database call, retrieval query, answer composition, or graph execution.
- No runtime promotion of Qdrant, hybrid retrieval, reranking, answer composer, or GraphRAG.
