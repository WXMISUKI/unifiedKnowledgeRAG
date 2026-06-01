# Phase 6 Qdrant+BGE-M3 Private-Network Promotion Review Contract

## Scope

- Phase: `Phase 6 / Deployment And Operations` with `Phase 3 promotion bridge`
- Type: read-only promotion review contract
- Goal: define required evidence inputs before Qdrant+BGE-M3 private-network candidate promotion review

## Non-goals

- Do not switch runtime defaults to `qdrant`, `bge_m3_local`, or hybrid retrieval.
- Do not start Qdrant, download model artifacts, run backup/restore operations, or execute deployment automation.
- Do not move control-plane responsibilities (registration, governance, audit, source binding, final policy) into this provider.

## Required Evidence Inputs

### 1) Qdrant Readiness Inputs

- `phase6-qdrant-vector-store-readiness` export exists and is parseable.
- `phase6-qdrant-backup-restore-smoke` exists and is parseable.
- Deployment and reindex linkage remain visible.

Recommended action when missing: `refresh_phase6_qdrant_readiness_chain`.

### 2) BGE-M3 Readiness Inputs

- `phase6-bge-m3-artifact-readiness` export exists and is parseable.
- `phase6-bge-m3-vs-mock-fixture-diagnostics` export exists and is parseable.
- `phase6-bge-m3-comparison-smoke` exists and is parseable.

Recommended action when missing: `refresh_phase6_bge_m3_readiness_chain`.

### 3) Phase 3 Quality/Latency Inputs

- Phase 3 runtime diagnostics evidence is available.
- Phase 3 latency/resource diagnostics evidence is available.
- FP/FN and hybrid calibration context remain available for interpretation.

Recommended action when missing: `refresh_phase3_candidate_evidence_chain`.

### 4) Deployment-Linkage Inputs

- Deployment readiness report is available in the same review cycle.
- Deployed smoke may be absent in local stage, but that absence must remain explicit as `review`.

Recommended action when missing: `refresh_deployment_linkage_evidence`.

## Review States

- `ready_for_private_network_candidate`: all required evidence inputs are present, parseable, and internally consistent.
- `review`: evidence exists but open gates remain or optional live evidence is missing.
- `blocked`: one or more critical required evidence inputs are missing or contradictory.

## Decision Boundary

This contract governs private-network promotion review readiness only. It does not approve runtime default promotion. Until separate promotion gates close, keep `decision=keep_runtime_defaults`.
