## Context

前两次真实 source 验证已经证明：

- onboarding 模板不是纸面能力
- 新 source 可以进入现有 baseline 路径

但为了让“通用 provider”这个结论更稳，我们还需要一种更不同的 source 类型。相比退款规则和物流 FAQ，规则/制度型 source 更接近很多企业知识库中的常见文档形态：

- 内容较短
- 规则明确
- 可做 identifier / role / negative-control 组合验证

因此本次选择新增一个轻量的 `invoice_policy_faq` markdown source，专门用于验证模板链路，而不是为了扩业务覆盖。

## Goals / Non-Goals

**Goals:**

- 选择一个与前两个验证 source 不同类型的新轻量 source。
- 用该 source 跑通 onboarding -> baseline 的最小验证路径。
- 证明模板链路对规则型 source 同样有效。
- 保持 provider 轻量和 evidence-first。

**Non-Goals:**

- 不并入主 aggregate baseline。
- 不新增 failed-question 或 confirmation 的真实填充，除非 baseline 本身暴露必要性。
- 不改 runtime defaults。
- 不做 query rewrite、rerank、hybrid retrieval、GraphRAG。
- 不把这个 source 扩展成业务级长期运营资产。

## Decisions

### 1. 直接新增一个极小 markdown source

由于仓库现有 source 类型有限，本次直接新增一个极小的规则型 source，而不是等待未来外部素材。

原因：

- 能快速验证模板通用性
- 范围可控
- 不引入 parser、ingestion 或更重依赖

### 2. 仍只做最小 baseline

该 source 仅补：

- 2 条 answerable
- 1 条 negative control

原因：

- 当前目标是模板链路验证
- 不是完成新 source 的全面业务评估

### 3. 最小 provider 可见性原则不变

只在以下三个点做最小补充：

- source catalog
- source document manifest
- fixture retriever

原因：

- 继续验证“新 source 能进入现有 provider 路径”
- 不引入独立的专用验证逻辑

## Validation Shape

`invoice_policy_faq` baseline 至少包括：

- 1 条发票时效/开票流程类 answerable
- 1 条发票抬头/材料类 answerable
- 1 条与采购/税务外部流程相关的 expected-empty negative control

## Risks / Trade-offs

- [新增 source 会不会变成业务扩面] -> 本次不并入 aggregate baseline，只作为模板链路验证样本。
- [source 太小，代表性有限] -> 当前目标是通用性验证，不是完成制度型知识库质量评估。
- [后续 catalog/注册逻辑仍然手动] -> 这是后续单独小切片的问题，本次不扩大范围。
