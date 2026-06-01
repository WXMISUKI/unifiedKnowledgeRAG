# Phase 8 Live URL Validation Decision Record

- Decision ID: `phase8-live-url-validation-decision-record-v1`
- Decision Date: `2026-06-01`
- Scope: `deployed live-url validation review`
- Decision: `keep_runtime_defaults_until_live_url_validation`
- Status: `approved-for-current-slice`

## Current Validation Snapshot

| Item | Current Value |
|---|---|
| Phase 8 execution contract | `ready` |
| Phase 8 readiness export | `review` (`live_validation_state=await_live_url_validation`) |
| Phase 8 smoke consistency check | `ready` |
| Runtime default promotion | `not approved` |

## Evidence Basis

| Evidence | Current Status | Key Signal |
|---|---|---|
| `phase8-live-url-validation-execution-contract` | `ready` | live URL execution scope and status semantics are explicit |
| `phase8-live-url-validation-readiness` | `review` | `deployed_smoke_present=false`, `live_url_present=false`, `open_gate_count=3` |
| `phase8-live-url-smoke-consistency-check` | `ready` | `10/10` consistency checks passed |
| `phase6-deployed-field-validation-readiness` | `review` | `field_validation_state=await_live_url` |
| `phase7-provider-release-readiness` | `review` | `release_state=ready_for_local_handoff` but promotion gates remain open |

## Open Gates

1. 真实部署 URL 的 `deployed_provider_smoke` 仍缺失，live-url 证据尚未闭环。
2. Phase 6 deployed field-validation 仍在 `await_live_url`。
3. Phase 7 release-readiness 仍保留 promotion 相关 open gates。

## Decision Outcome

本轮 Phase 8 结论是：live-url 验证契约与本地一致性检查已经完备，但现场 URL 证据尚未补齐，因此继续保持 `keep_runtime_defaults_until_live_url_validation`。当前结论不等于 runtime default promotion 批准。

## Next-Step Entry Conditions

1. 在真实部署 URL 上执行并产出 `deployed-provider-smoke` 证据。
2. 重新导出 Phase 8 readiness 与 Phase 8 smoke consistency，确认 open gates 收敛。
3. 在独立 promotion change 中评估 runtime default switch，不与 live-url 验证混并决策。
