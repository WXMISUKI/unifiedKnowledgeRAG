## Context

当前 provider 已经把评估治理层抽象出来了，但还缺“用一个新真实 source 验证模板链路”的证据。这一步如果不做，我们虽然有模板、有 catalog，但仍可能停留在“对当前几个 source 适配得很好”的状态。

`split_refund_policy_docs` 适合作为验证对象，因为：

- 内容轻量
- 结构清晰
- 已有真实 source 文件
- 与当前主 baseline 的 source 集合不同

这一步的目标不是把它扩成新的大规模业务闭环，而是验证：

- onboarding 模板是否真能指导新 source 接入
- 最小 baseline 是否能产出
- provider 是否只需很少的增量可见性补充

## Goals / Non-Goals

**Goals:**

- 用一个新的真实 source 验证 onboarding 模板路径。
- 为这个 source 产出最小 baseline fixture 与报告。
- 证明 provider 只需少量增量配置即可承载新 source baseline。
- 保持项目仍然是通用 provider，而不是 source-specific 优化。

**Non-Goals:**

- 不把 `split_refund_policy_docs` 直接并入主 aggregate baseline。
- 不新增 failed-question pack 或 confirmation pack 的真实填充，除非 baseline 本身暴露了必要性。
- 不改 query rewrite、rerank、hybrid retrieval、GraphRAG。
- 不调整现有 runtime defaults。

## Decisions

### 1. 只验证最小 baseline，不扩成完整 source workstream

当前仅为 `split_refund_policy_docs` 建立最小 baseline fixture 和报告。

原因：

- 先证明模板链路可用
- 避免一次性把它扩展成新的 aggregate source
- 保持这个切片小而完整

### 2. 通过最小 provider 可见性补充支持 baseline

为了让现有 baseline 能直接复用，需要让 provider 在：

- source catalog
- source document manifest
- fixture retriever

三个地方对 `split_refund_policy_docs` 可见。

原因：

- 这比新建专用评估引擎更轻
- 也更符合“新 source 真能进入现有 provider 路径”的验证目标

### 3. 不立即把新 source 纳入 catalog 的固定 pack 集合

当前 catalog 仍保持已有固定 pack 视图，这个 change 主要验证模板接入和真实 baseline。

原因：

- catalog 自动发现/注册是后续可能的单独小切片
- 本次先证明真实 source onboarding 成功

## Validation Shape

本次 baseline 至少包含：

- 1 条 answerable exact-identifier / form query
- 1 条 answerable related process/material query
- 1 条 expected-empty negative control

这样既能验证 source 可答能力，也能验证 fail-closed 行为。

## Risks / Trade-offs

- [把 evaluation-only source 暴露给 provider list] -> 这是有意的最小可见性补充，但仍不代表 runtime strategy promotion。
- [baseline 太小，不能代表完整 source 质量] -> 当前目标是验证模板链路，不是完成全面评估。
- [catalog 尚未自动纳入这个新 source] -> 当前切片刻意不做 bridge，避免 scope 膨胀。
