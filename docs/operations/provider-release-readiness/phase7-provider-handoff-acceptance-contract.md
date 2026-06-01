# Phase 7 Provider Handoff Acceptance Contract

- Report: `phase7-provider-handoff-acceptance-contract-v1`
- Status: `review`
- Scope: `cross-phase handoff acceptance`
- Generated At: `2026-06-01`

## Purpose

This contract defines how callers and deployment reviewers should consume the provider handoff evidence chain across Phase 2 to Phase 6.
It is intentionally read-only and acceptance-oriented. It does not promote runtime defaults.

## Required Evidence

The following artifacts are required for local handoff acceptance:

1. `provider_integration_probe`
2. `provider_contract_smoke`
3. `source_binding_summary`
4. `provider_handoff_bundle`

These are the minimum evidence gates for "can this provider be handed off locally as a lightweight external knowledge component."

## Optional Review Evidence

The following artifacts are optional but strongly recommended for richer review context:

1. Phase 2 source-format demand readiness and unsupported-format negative-control smoke
2. Phase 3 retrieval promotion readiness, runtime diagnostics, latency/resource diagnostics, and promotion decision artifacts
3. Phase 4 evidence pack readiness and caller-consumption smoke
4. Phase 5 graph use-case readiness and graph boundary smoke summary
5. Phase 6 deployment/deployed-field/private-network review artifacts

Optional artifacts should not be interpreted as "ignored"; they are review amplifiers, not required local-handoff blockers.

## Acceptance Semantics

| Status | Meaning |
| --- | --- |
| `ready` | Evidence chain for this artifact is complete and currently passes its checks |
| `review` | Evidence is present but still needs human judgment or downstream gates |
| `blocked` | Artifact failed or missing required prerequisites |

Global guidance for this cycle:

1. `ready_for_local_provider_handoff` can be true while some optional artifacts remain `review`.
2. `ready_for_runtime_default_promotion` remains false unless separate promotion gates are explicitly closed.
3. deployed live URL smoke remains a separate field-validation gate and is not auto-satisfied by local evidence.

## Ownership Boundary

This provider remains a lightweight evidence/data plane.
Caller/control-plane ownership remains external for:

1. provider registration and heartbeat governance
2. audit and policy workflows
3. source-to-agent binding decisions
4. final user-facing answer policy and orchestration

## Non-Goals

1. Runtime default promotion for Qdrant/BGE-M3/hybrid
2. Graph query execution rollout
3. Parser expansion rollout beyond Markdown baseline
4. Deployment certification replacement for real live URL smoke
