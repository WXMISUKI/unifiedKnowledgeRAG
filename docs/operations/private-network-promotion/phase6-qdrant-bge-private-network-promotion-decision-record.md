# Phase 6 Qdrant+BGE Private-Network Promotion Decision Record

## Cycle

- Date: `2026-06-01`
- Scope: private-network promotion review for Qdrant+BGE evidence chain

## Verdict

- Decision: `keep_runtime_defaults`
- Review State: `review`
- Runtime default changes: `none`

## Evidence Basis

- private-network promotion review contract
- private-network promotion readiness export
- private-network promotion smoke
- qdrant vector-store readiness and backup/restore smoke
- bge-m3 artifact/comparison diagnostics/smoke
- phase3 runtime and latency diagnostics
- deployment readiness and optional deployed smoke policy

## Open Gates

- deployed private-network URL smoke evidence is still optional/missing in local phase
- promotion remains candidate-level until live deployment validation and reviewer sign-off
- hybrid runtime promotion remains a separate phase and has not started

## Next-Phase Entry Conditions

- private-network promotion readiness reaches `ready_for_private_network_candidate`
- deployed smoke evidence is available for the target environment or explicitly waived by review policy
- phase3 candidate quality/latency controls remain stable after latest evidence refresh

## Boundary Reminder

This record is documentation-only governance evidence. It does not switch runtime defaults, does not execute deployment actions, and does not move control-plane ownership into this provider.
