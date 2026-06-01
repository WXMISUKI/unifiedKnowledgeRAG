## Summary

Implement a read-only export that consolidates private-network promotion review inputs for Qdrant+BGE-M3 into a single readiness artifact.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations, bridging to Phase 3 promotion review.
- Nature: local evidence visibility export.
- Non-goal: runtime default promotion.

## Data Inputs

- Qdrant vector-store readiness and backup/restore smoke.
- BGE-M3 artifact readiness, comparison diagnostics, and comparison smoke.
- Phase 3 runtime/latency diagnostics and FP/FN review.
- Deployment readiness and optional deployed smoke.
- Private-network promotion review contract presence.

## Output

- `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json`
- `docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.md`

## Status Semantics

- `blocked`: critical required evidence is missing.
- `review`: evidence exists but open gates remain.
- `ready_for_private_network_candidate`: required evidence is complete and internally consistent.
