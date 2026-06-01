## Summary

Add a compact read-only smoke artifact that checks private-network promotion evidence-chain completeness for Qdrant+BGE review.

## Phase Alignment

- Roadmap phase: Phase 6 operations with Phase 3 bridge support.
- Nature: local smoke evidence maintenance.
- Non-goal: promotion execution or runtime default switching.

## Smoke Inputs

- private-network promotion review contract
- private-network promotion readiness export
- qdrant vector-store readiness
- qdrant backup/restore smoke
- bge artifact readiness
- bge comparison diagnostics
- bge comparison smoke
- phase3 runtime and latency diagnostics
- deployment readiness

## Output

- `docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.json`
- `docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.md`
