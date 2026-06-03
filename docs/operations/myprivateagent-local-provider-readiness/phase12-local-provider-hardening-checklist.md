# Phase 12 MyPrivateAgent Local Provider Hardening Checklist

## Scope

- Phase: `Phase 12 / MyPrivateAgent Local RAG Integration Hardening`
- Audience: provider 侧接入管理与控制者
- Review Mode: 只读本地消费链路校验

## Local URL / API-Key Deterministic Fallback

- 推荐本地消费端点：`http://127.0.0.1:8020`
- 本地默认运行模式允许 `PROVIDER_API_KEY` 缺失（`not_configured_local_dev`）。
- 当切到保护模式（`PROVIDER_API_KEY` 配置后）：
  - 认证入口可使用 `Authorization: Bearer <token>` 或 `X-Provider-Api-Key: <token>`；
  - 接入方应保持一致的 header 约定以避免本地验证漂移。

## Provider Readiness Verification

建议按固定顺序完成以下核验后再判定本地 provider-ready（仅用于本地接入评审）：

1. `GET /api/provider/preflight` 中 `bindable` 与 `checks` 已落地；
2. `GET /api/provider/source-bindings` 显示 `source_binding_summary` 可读取；
3. `GET /api/provider/handoff` 能返回本地 handoff bundle，并确认新增 `phase12_local_rag_integration_hardening_profile` 作为可选项可见；
4. 本地证据链闭环：
   - `phase11_local_provider_integration_profile`
   - `phase11_provider_discovery_smoke`
   - `phase11_rag_retrieve_consumption_smoke`
   - `phase11_source_binding_preview_smoke`
   - `phase12_local_rag_integration_hardening_profile`
   - `phase12_local_rag_integration_hardening_smoke`

## Local Hardening Acceptance

- 只要上述证据链显示 `ready/review`，并明确边界保守（不改 runtime），即可进入本地 hardening review 阶段。
- 只有在调用方明确要求进行 deployment/production promotion 时，才启动下一阶段的 runtime 候选切换评审。

## Boundary Reminder

- 本阶段保持 runtime defaults（qdrant / BGE-M3 / hybrid / aggregation / relation-aware）不切换；
- 本阶段不做 GraphRAG query 执行；
- 无权修改 source-to-agent 绑定策略和调用方编排策略。
