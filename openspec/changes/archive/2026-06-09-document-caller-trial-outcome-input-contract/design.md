## Context

我们已经明确当前 provider 应进入 hold-state，后续 reopen 必须依赖更强的真实触发器。对本仓库来说，最重要的触发器来源不是新的 provider 内部能力，而是 caller 侧真实 trial 的结果回流。

当前已有能力：

- Phase 15: repo-side trial dispatch package
- Phase 16: minimal access loop
- Phase 25: live trial outcome feedback closure

缺失的是：

- 一个稳定、明确、对调用方友好的 trial outcome 输入合同

这意味着现在最合理的下一步，是把“如何产生 provider 可消费的 trial outcome JSON”变成正式资产，而不是继续在 provider 内部扩能力。

## Goals / Non-Goals

**Goals:**

- 定义 Phase 25 所依赖的 caller trial outcome 最小输入结构。
- 明确 required / optional 字段，以及 provider 如何解释这些字段。
- 给出一份可复制的 example JSON，降低调用方接入成本。
- 让 Phase 25 的 fail-closed 逻辑更清晰，避免弱输入被误判为 provider 正常。

**Non-Goals:**

- 不执行 MyPrivateAgent。
- 不创建跨仓库自动同步机制。
- 不扩展 provider runtime 功能。
- 不处理 final answer policy、binding policy、approval/audit 等 caller/control-plane 职责。
- 不引入新的 retrieval / rerank / hybrid / GraphRAG 能力。

## Decisions

### 1. 以“文档合同 + 样例 + 最小校验增强”组成完整切片

只写一份说明文档不够，因为调用方仍可能自己猜字段；只改代码也不够，因为外部协作方缺少正式约定。

因此这次切片同时包含：

- 文档合同
- example JSON
- 现有 Phase 25 解析逻辑的最小增强

### 2. 合同只定义 provider 真正依赖的最小字段

我们不应该把 trial outcome 设计成重型平台协议。

本次合同只保留 provider 判断必需字段，例如：

- `live_trial_status`
- `reason_code`
- `provider_base_url`
- `agent_id`
- `query`
- `provider_retrieve.status`
- `provider_retrieve.reason_code`
- `provider_retrieve.document_count`
- `provider_retrieve.evidence_pack_status`
- `provider_retrieve.citation_policy`
- `provider_retrieve.allowed_citations`

其他字段保持可选，以保持轻量与通用。

### 3. 对关键字段缺失采用 fail-closed review/block 策略

如果输入文件只是“存在”，但关键字段缺失，provider 不应乐观判为 `ready`。

因此应增强 Phase 25：

- 缺少关键 trial 状态或 retrieve 状态时，进入保守分类
- 将字段缺失记录为 warning 或 blocker
- 保持当前的 provider/caller 边界不变

### 4. 该切片服务的是“真实反馈闭环”，不是下一轮 readiness 链

这次工作不是重新开一个 readiness phase，而是把反馈入口固定下来。

这样后续若出现：

- `provider_review_required`
- `provider_blocked`

我们就能基于真实输入判断是否要 reopen provider。

## Risks / Trade-offs

- [合同写太细，变成重协议] -> 只定义 provider 判定真正需要的最小字段。
- [合同写太松，调用方仍然随意] -> 通过 example 和 focused tests 明确最小要求。
- [继续偏文档化] -> 这次文档是为了真实调用反馈闭环服务，不是为了增加 provider 内部抽象层。
