# Phase 7 Provider Release Decision Record

- Decision ID: `phase7-provider-release-decision-record-v1`
- Decision Date: `2026-06-01`
- Scope: `cross-phase provider handoff and release review`
- Decision: `ready_for_local_provider_handoff_but_not_runtime_promotion`
- Status: `approved-for-current-slice`

## Current Release Snapshot

| Item | Current Value |
|---|---|
| Phase 7 acceptance contract | `ready` |
| Phase 7 release-readiness export | `review` (`release_state=ready_for_local_handoff`) |
| Phase 7 cross-phase consistency smoke | `ready` |
| Runtime default promotion | `not approved` |

## Evidence Basis

| Evidence | Current Status | Key Signal |
|---|---|---|
| `phase7-provider-handoff-acceptance-contract` | `ready` | required vs optional handoff semantics are explicit |
| `phase7-provider-release-readiness` | `review` | `ready_for_local_provider_handoff=true`, `ready_for_runtime_default_promotion=false` |
| `phase7-cross-phase-handoff-consistency-smoke` | `ready` | cross-phase decision/smoke alignment checks pass |
| `phase3-hybrid-runtime-promotion-decision-record` | `review posture` | current cycle remains `keep_runtime_defaults` |
| `phase6-deployed-field-validation-readiness` | `review` | live URL validation gate remains open |

## Open Gates

1. Runtime default promotion still needs stronger customer-like benchmark and deployment-side evidence.
2. Live deployed URL smoke evidence is still required for field validation closure.
3. Candidate promotion remains evidence-review-only until those gates are explicitly closed.

## Decision Outcome

本轮 Phase 7 结论是：provider 已具备本地交接可用的跨阶段证据链，但不具备 runtime default promotion 条件。我们保持 `keep_runtime_defaults`，并将生产提升继续放在后续独立 gate 变更中推进。

## Next-Step Entry Conditions

1. 完成真实部署 URL 的 deployed smoke 与 field-validation 收口。
2. 在更接近客户语料条件下补齐 promotion 级 benchmark 和 FP/FN 复核。
3. 在独立 promotion change 中明确记录并批准 runtime default switch。
