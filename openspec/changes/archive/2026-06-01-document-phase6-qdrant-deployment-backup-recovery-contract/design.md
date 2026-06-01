## Summary

Add a Phase 6 Qdrant deployment/backup/recovery readiness contract that turns scattered operations guidance into one reviewable boundary document.

## Phase Alignment

- Roadmap phase: Phase 6 deployment and operations.
- Nature: documentation-only readiness contract.
- Non-goal: enabling Qdrant as runtime default, automating backup/restore, or adding control-plane governance logic.

## Decisions

- Keep the contract read-only and evidence-first.
  It defines required evidence and review gates; it does not execute Qdrant actions.

- Separate process readiness from promotion readiness.
  Qdrant can be deployed and recoverable while runtime defaults still remain `fixture/mock`.

- Preserve external ownership boundaries.
  Provider offers diagnostics and evidence; control-plane decisions stay outside this repository.

## Contract Coverage

- Deployment surface: endpoint/private-network posture, collection/vector config, secret redaction expectations.
- Backup posture: snapshot location, retention expectation, checksum/manifests, operator ownership.
- Recovery posture: restore drill evidence, replay/reindex linkage, failure handling notes.
- Promotion linkage: explicit note that Qdrant readiness is prerequisite evidence, not promotion approval.

## Output

- Markdown contract:
  `docs/operations/qdrant-vector-store-readiness/phase6-qdrant-deployment-backup-recovery-contract.md`
