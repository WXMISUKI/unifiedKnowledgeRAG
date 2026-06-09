## Context

我们已经完成了：

- source onboarding 模板生成
- 多个真实 source 的最小 onboarding validation
- source onboarding catalog
- pack catalog 和 onboarding summary bridge

因此当前最明显的轻量缺口不是更多 catalog 层抽象，而是 `source_template_example` 这个示例本身还停留在模板态。对一个强调通用 provider、低接入成本、evidence-first 的项目来说，把它补成最小真实 baseline 示例，会比继续做 source-specific hardening 或高级检索策略更合适。

## Goals / Non-Goals

**Goals:**

- 把 `source_template_example` 提升为一个真实但极小的 baseline onboarding 示例。
- 保持内容简短、规则型、可验证。
- 让 source onboarding catalog 不再把它标记为 `template_only`。
- 让 pack catalog 的 onboarding summary 同步反映该变化。

**Non-Goals:**

- 不把该 source 并入 aggregate real-business baseline。
- 不新增 failed-question 或 confirmation 的真实填充。
- 不改 runtime defaults。
- 不做 query rewrite、rerank、hybrid retrieval、GraphRAG。
- 不把它扩展成长期业务资产或复杂示范工程。

## Decisions

### 1. 直接让 `source_template_example` 成为一个最小真实 source

不再保留它为纯占位名字，而是让它对应一个极小 markdown source。

原因：

- 这样最符合“标准 onboarding 示例”的定位
- 不需要再创建额外示例 id
- 目录和产物结构都能继续复用

### 2. 内容保持规则型、短小、可 fail-closed

延续前两条验证切片的风格：

- 2 条 answerable
- 1 条 expected-empty

原因：

- 当前目标是闭环示例，不是扩业务面
- 这样最利于快速验证与后续复用

### 3. 仍然只补最小 provider 可见性

仅更新：

- source catalog
- source package
- source document manifest
- fixture retriever

原因：

- 继续复用现有 provider 路径
- 不创造专用示例逻辑

## Risks / Trade-offs

- [示例 source 名称较抽象] -> 接受，这是标准 onboarding 示例，不是业务资产。
- [把模板样本变成真实 source 可能看起来像扩 source] -> 通过文档与 spec 明确其定位是“通用示例闭环”而非业务扩展。
- [后续可能仍有人想继续堆更多模板示例] -> 当前只做一个闭环示例，避免进入样板数量优化。
