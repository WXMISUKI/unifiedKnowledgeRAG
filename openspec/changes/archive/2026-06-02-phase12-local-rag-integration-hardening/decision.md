# Phase 12 Local RAG Integration Hardening Decision Record

## Decision

- Decision time: `2026-06-02`
- Decision scope: `phase12-local-rag-integration-hardening`
- Verdict: `keep_local_rag_integration_review_only`
- Keep runtime defaults unchanged (`mock` embedding/retrieval/backend defaults remain in place).

## Evidence Reviewed

- `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-profile.json`
- `docs/smoke/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-smoke.json`
- `docs/integration/provider-handoff/provider-handoff-bundle.json`
- `docs/integration/myprivateagent-local-provider-integration/phase11-local-provider-integration-profile.json`
- `docs/smoke/myprivateagent-local-provider-integration/phase11-provider-discovery-smoke.json`
- `docs/smoke/myprivateagent-local-provider-integration/phase11-rag-retrieve-consumption-smoke.json`
- `docs/smoke/myprivateagent-local-provider-integration/phase11-source-binding-preview-smoke.json`
- `docs/integration/myprivateagent-local-consumer-verification/phase10-myprivateagent-local-consumer-readiness.json`

## Decision Logic

- The phase12 hardening profile is currently `blocked` because required phase11/phase10/profile/bundle signals are not fully ready.
- The phase12 hardening smoke is currently `blocked` because the handoff bundle is blocked.
- The new hardening row is integrated into:
  - `docs/integration/provider-handoff/provider-handoff-bundle.json` (optional artifact row)
  - `docs/integration/provider-handoff-refresh/provider-handoff-refresh.md|json` (optional step with `review` mapping for blocked source).
- No source-to-agent binding policy, source-binding decisions, audit policy, or runtime HTTP behavior is changed in this phase.

## Local Assumptions Recorded

- Recommended local endpoint: `http://127.0.0.1:8020`.
- API mode:
  - `not_configured_local_dev` when `PROVIDER_API_KEY` 未设置。
  - `provider_key_protected_api` when key is configured（`Authorization: Bearer <token>` 或 `X-Provider-Api-Key: <token>`）。
- Failover rule: hardening blockers are reviewed locally; this phase is evidence-only and non-blocking for runtime promotion.

## Open Gates (blocking review)

- `phase10_local_consumer_readiness`
- `phase11_local_provider_integration_profile`
- `phase6_deployed_field_validation_readiness`（在 handoff 闭环中作为链路上游持续开放）
- `deployed_provider_smoke`（可选，但用于完整闭环）

## Next Actions

- 1) 运行 `python scripts/export_phase12_local_rag_integration_hardening_profile.py`
   and `python scripts/export_phase12_local_rag_integration_hardening_smoke.py`；
- 2) 运行 `python scripts/export_provider_handoff_bundle.py` and `python scripts/export_provider_handoff_refresh.py`
  to keep handoff artifacts aligned after each evidence refresh；
- 3) 完成 local hardening review-only 阶段后，方可进入下一阶段的 backend 候选评估（不触发 runtime promotion）。
