## Summary

Implement a read-only Phase 6 Qdrant vector-store readiness export that consolidates existing local evidence into one review artifact.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: local evidence visibility export.
- Non-goal: runtime promotion, live backup/restore execution, or control-plane workflow ownership.

## Data Sources

- `docs/operations/deployment-readiness/deployment-readiness.json`
- `docs/operations/reindex-readiness/reindex-readiness.json`
- `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-deployment-backup-recovery-contract.md`
- `docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json` (optional benchmark context)

## Output

- `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json`
- `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.md`

## Status Rules

- `blocked`: contract missing, or critical deployment/reindex evidence missing.
- `review`: evidence exists but still candidate/mock/fixture or review gates open.
- `ready`: deployment and reindex are ready, contract present, and Qdrant candidate evidence exists with no open review gates.

Default expectation in local dev remains `review`.
