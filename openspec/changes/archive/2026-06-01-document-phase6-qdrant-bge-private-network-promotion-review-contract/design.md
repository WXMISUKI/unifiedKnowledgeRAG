## Summary

Define a Phase 6 private-network promotion review contract that consolidates Qdrant and BGE-M3 evidence requirements before any runtime promotion decision.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations with explicit Phase 3 promotion bridge value.
- Nature: documentation-only readiness contract.
- Non-goal: enabling runtime defaults, starting Qdrant, downloading models, or executing control-plane policy.

## Decisions

- Keep review read-only and evidence-first.
  The contract describes what must be reviewed; it does not execute runtime changes.

- Preserve optional deployed-smoke behavior for local phase.
  Missing deployed URL evidence stays explicit as `review`, not hidden pass/fail.

- Keep promotion decision separate.
  This contract supports promotion review but does not approve default promotion.

## Review Inputs

- Qdrant vector-store readiness and backup/restore smoke.
- BGE-M3 artifact readiness, comparison diagnostics, and comparison smoke.
- Phase 3 runtime/latency/FP-FN comparison context.
- Deployment readiness and optional deployed smoke.
