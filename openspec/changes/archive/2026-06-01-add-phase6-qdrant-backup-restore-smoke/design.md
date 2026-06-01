## Summary

Add a lightweight Phase 6 smoke summary for Qdrant backup/restore readiness that checks local prerequisite evidence without performing live backup/restore actions.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: read-only smoke evidence maintenance.
- Non-goal: executing Qdrant snapshot or restore commands.

## Checks

- Qdrant deployment/backup/recovery contract exists.
- Qdrant vector-store readiness export exists and is parseable.
- Deployment readiness is available.
- Reindex readiness is available.

## Output

- `docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json`
- `docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.md`
