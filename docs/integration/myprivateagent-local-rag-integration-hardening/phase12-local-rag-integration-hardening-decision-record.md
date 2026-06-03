# Phase 12 Local RAG Integration Hardening Decision Record

## Decision

- Decision ID: `phase12-local-rag-integration-hardening-decision-record-v1`
- Decision Date: `2026-06-02`
- Scope: `myprivateagent local RAG integration hardening readiness (local-only)`
- Current verdict: `ready_for_local_rag_integration_hardening_review`
- Runtime default changes: `none`

## Evidence

- Contract: `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-contract.md`
- Profile: `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-profile.json`
- Smoke: `docs/smoke/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-smoke.json`
- Handoff bundle (optional status row): `docs/integration/provider-handoff/provider-handoff-bundle.json`

## Posture

- Recommended local base URL: `http://127.0.0.1:8020`
- Local API-key mode: `not_configured_local_dev` is acceptable for local smoke and local hardening checks.
- Deployment/API protected mode, when enabled, should use `PROVIDER_API_KEY` with one of:
  - `Authorization: Bearer <token>`
  - `X-Provider-Api-Key: <token>`

## Decision Outcome

本轮 Phase 12 结论是：本地 hardening 检查链路可用于 MyPrivateAgent 本地接入评审（`ready_for_local_rag_integration_hardening_review`），并且明确继续保持“证据只读、无 runtime 默认推广”的边界。  
当前结果未闭环 runtime promotion，仍受 `phase10`/`phase11`/`provider_handoff_bundle` 等上游 open gates 限制。

## Next-Step Entry Conditions

1. 完成本地 MyPrivateAgent 端点消费链路核验后，更新 `phase12` profile 的 open_gate_count 并重跑：
   - `python scripts/export_phase12_local_rag_integration_hardening_profile.py`
   - `python scripts/export_phase12_local_rag_integration_hardening_smoke.py`
2. 重跑 provider handoff 行为链（含新增行）后，检查手工消费清单和 handoff refresh 阶段行是否出现：
   - `python scripts/export_provider_handoff_refresh.py`
3. 按 `docs/operations/myprivateagent-local-provider-readiness/phase12-local-provider-readiness-hardening-checklist.md` 和  
   `docs/operations/myprivateagent-consumption-readiness/phase12-myprivateagent-consumption-hardening-checklist.md` 进行本地验证。
