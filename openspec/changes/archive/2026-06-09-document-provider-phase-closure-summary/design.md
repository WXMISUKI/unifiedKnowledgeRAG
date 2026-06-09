## Context

当前 provider 已经把“轻量、通用、evidence-first”的主链闭合到了一个比较健康的状态：

- 有通过的 breadth baseline
- 有单独的 failed-question baseline
- 有 confirmation baseline
- 有 source evaluation pack catalog
- 有通用 onboarding scaffold
- 有多个真实 source 证明 onboarding path 可复用
- 有 onboarding discovery 与 pack discovery 的轻量 bridge
- 有 provider next-step trigger contract

这说明当前系统的核心问题已经不是“能力缺块”，而是“如何防止继续围绕同一局部做无止境补强”。

## Goals / Non-Goals

**Goals:**

- 输出一份正式的 provider 阶段收口总结文档。
- 把当前已完成能力、冻结边界、reopen triggers、下一步推荐方向明确下来。
- 让未来协作者可以从单一入口快速判断：现在是否应该继续做 provider。
- 把 `RAG_Techniques` 的经验使用方式重新收敛为“失败模式驱动、证据驱动、非默认启用高级技术”。

**Non-Goals:**

- 不新增任何 provider runtime 行为。
- 不新增 source、pack、catalog、query rewrite、rerank、hybrid retrieval、GraphRAG。
- 不把 caller/control-plane 问题重新写回 provider 待办。
- 不重开新的 access-readiness 链路。

## Decisions

### 1. 本切片是“阶段总结切片”，不是“功能切片”

当前项目最正确的动作不是再补一个通用性小功能，而是把这一阶段的共识转成正式文档资产。

这样做的收益：

- 降低后续重复讨论成本
- 给未来的 reopen 决策提供统一参考入口
- 防止 provider 被持续推向重型平台

### 2. 阶段收口文档必须服务“未来 reopen 决策”

收口文档不是简单的工作总结，而是一个未来 decision entrypoint。它至少要回答：

- 当前已经完成了哪些能力闭环
- 当前为什么不继续扩 provider
- 哪些触发器成立时才允许 reopen
- 哪些问题明确不该回流到本仓库
- 当前推荐的下一阶段动作是什么

### 3. 下一阶段动作应偏向“持有基线”，而不是“继续构建”

结合当前项目设计目标和 `RAG_Techniques` 经验，下一阶段最合理的方向不是继续扩 provider，而是：

- 持有当前 provider baseline
- 等待真实 caller 或真实失败模式提供新触发器
- 如果未来要评估高级 RAG 技术，必须先有重复真实失败证据

### 4. 把经验沉淀转化为“策略候选原则”，而不是“实施清单”

`RAG_Techniques` 的价值在于提供 strategy candidates，而不是要求我们顺序实现 query rewrite、HyDE、rerank、GraphRAG。

因此本次收口会进一步明确：

- 这些技术保留为候选策略库
- 没有触发器时不进入实现待办
- 当前 provider 的首要目标是维持“通用、轻量、可用”

## Risks / Trade-offs

- [看起来推进较慢] -> 这是主动收口，不是停滞；它防止项目继续在局部打转。
- [文档很多、功能没有增加] -> 当前阶段最缺的是统一判断入口，而不是新的 provider 功能。
- [未来协作者可能忽略该总结] -> 通过更新路线图、规格和进度台账，把它变成正式入口而不是孤立笔记。
