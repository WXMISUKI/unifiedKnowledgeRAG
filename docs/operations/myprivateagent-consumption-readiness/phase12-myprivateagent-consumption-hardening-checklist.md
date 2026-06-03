# Phase 12 MyPrivateAgent Consumption Hardening Checklist

## Scope

- Phase: `Phase 12 / MyPrivateAgent Local RAG Integration Hardening`
- Audience: 本地调试使用者（myprivateagent consumer）
- Review Mode: 本地可重复、只读验证

## Local Endpoint and Auth Fallback

- 推荐本地 URL：`http://127.0.0.1:8020`
- 本地消费默认允许 `PROVIDER_API_KEY` 未配置（开发体验优先）：
  - `PROVIDER_API_KEY` 未配置：视为 `not_configured_local_dev`
  - `PROVIDER_API_KEY` 已配置：需在请求头提供 token（任一）：
    - `Authorization: Bearer <token>`
    - `X-Provider-Api-Key: <token>`
- `/api/*` 的受保护行为取决于 `PROVIDER_API_KEY` 是否配置；本地 hardening 阶段不要求立刻开启保护。

## Deterministic Verification Steps

每次本地复核请固定这三步：

1. 使用推荐 URL 访问 `GET /health` 和 `GET /api/provider/manifest`。
2. 按 `docs/integration/myprivateagent-local-rag-integration-hardening/phase12-local-rag-integration-hardening-profile.md` 确认：
   - `phase10_local_consumer_readiness`、`phase10_local_consumer_probe`；
   - `phase11_local_provider_integration_profile`；
   - `phase11_source_binding_preview_smoke`、`phase11_rag_retrieve_consumption_smoke`；
   - `provider_contract_smoke` 是否满足 `passed=true`。
3. 运行 hardening profile + smoke 导出并确认状态：
   - `phase12_local_rag_integration_hardening_profile`
   - `phase12-local-rag-integration-hardening-smoke`

## Fail-Fast Rules

- 本地环境未配置 `PROVIDER_API_KEY` 时，不应将失败归因于鉴权层；应以 hardening profile 中的 `open_gate_ids` 与 `api_key_mode` 做原因归类。
- 若任何硬化项 `status=blocked`，更新对应 evidence 后重跑，并仅在 `ready`/`review` 时继续后续验证链路。

## Ownership Boundary

- 本文档仅覆盖 provider-side hardening 证据与本地复核动作；
- 源到智能体绑定、注册、审批、审计策略仍由调用方（MyPrivateAgent 或控制面）承担；
- 不在本阶段进行 runtime default 切换。
