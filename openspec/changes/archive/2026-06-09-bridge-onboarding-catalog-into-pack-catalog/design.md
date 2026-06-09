## Context

当前 provider 已经有两类互补但分离的发现入口：

- source evaluation pack catalog：看 baseline / failed-question / confirmation pack
- source onboarding catalog：看 source onboarding 模板与最小验证状态

这两个视图都已经成立，但使用时仍需要来回切换。对于“轻量、证据优先、避免平台化”的项目目标来说，当前更合理的改进不是合并模型，而是做一个只读摘要桥接：让 pack catalog 能看见 onboarding 层的成熟度信号。

## Goals / Non-Goals

**Goals:**

- 在不改变 pack catalog 主语义的前提下，引入 onboarding 摘要字段。
- 让 pack catalog 直接暴露 onboarding source 总量、ready/template-only 数量和 ready source 列表。
- 在缺失 onboarding catalog 时保持 pack catalog 仍可独立工作。
- 保持桥接为 evidence-only discovery 增强。

**Non-Goals:**

- 不把 onboarding entries 合并成 pack entries。
- 不让 onboarding 状态改变 pack catalog 的核心 decision 规则。
- 不自动注册 source。
- 不自动并入 aggregate baseline。
- 不做新的 retrieval evaluation 或高级 RAG 策略变更。

## Decisions

### 1. 只读取 onboarding catalog 产物，不直接扫描 onboarding 目录

pack catalog 只读取已生成的 `source-onboarding-catalog.json`。

原因：

- 保持职责清晰
- 复用上一条切片已有的 discovery 结果
- 避免 pack catalog 再复制一套 onboarding 目录扫描逻辑

### 2. 桥接信号进入 summary，不进入 pack 列表

onboarding 信息只以 summary / optional section 方式呈现。

原因：

- pack list 仍代表 evaluation packs
- source onboarding entries 和 pack entries 不是同一层级对象
- 这样最不容易造成概念混淆

### 3. onboarding 缺失是可见但非阻断的附加信号

如果 onboarding catalog 缺失：

- pack catalog 仍按原逻辑导出
- 只补一个 `onboarding_catalog_present=false`

原因：

- 当前 bridge 是增强项，不是 pack catalog 的硬依赖
- 保持 provider 证据层的松耦合

## Risks / Trade-offs

- [两个 catalog 的摘要可能出现时间不同步] -> 明确这是本地证据快照，必要时一起刷新导出。
- [用户误以为 onboarding ready 就代表 runtime ready] -> 在 non-goals 和 summary 字段里继续强调 `source_registration_status=not_created` 与 `aggregate_baseline_expansion_status=not_expanded`。
- [pack catalog 变重] -> 只引入小量 summary 字段，不新增嵌套大对象，不改变 decision 规则。
