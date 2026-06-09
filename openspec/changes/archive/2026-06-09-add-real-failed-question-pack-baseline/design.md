## Context

项目当前已经完成三 source aggregate baseline 扩面，并维持 `decision=go`。这说明 provider 的轻量 baseline 能力已经足以承载多个真实业务域，但也意味着继续只扩“容易通过”的 source，会让后续高级技术选择缺少 failure evidence。结合 `RAG_Techniques` 经验，下一步更合理的是把真实失败候选问题单独沉淀为一个可重复执行的 baseline，而不是直接进入 query rewrite、rerank、hybrid retrieval 或 GraphRAG。

现有 `local_business_rag_golden_cases.py` 已经提供了：

- source-by-source conservative evaluation
- failure mode / risk level 汇总
- review observation 汇总

因此最小实现不需要新建一套评估引擎，只需要在现有 aggregate report 之上增加：

- 独立失败问题包 fixture
- question-origin 维度
- 独立导出入口与报告文件

## Goals / Non-Goals

**Goals:**

- 建立一个独立的真实失败问题包 baseline。
- 让失败问题可以携带来源和已观察失败描述，而不是只记录 query 本身。
- 让报告能够清楚呈现“现在出现了哪些 failure-driven 信号”。
- 保持 provider 轻量、可回退、evidence-first。

**Non-Goals:**

- 不引入 query rewrite、HyDE、HyPE。
- 不引入 rerank、fusion/hybrid retrieval。
- 不改变 chunking default。
- 不引入 GraphRAG、RAPTOR、Self-RAG、CRAG。
- 不改变公共 HTTP API。
- 不把 caller/control-plane 责任移入 provider。

## Decisions

### 1. 失败问题包复用现有 aggregate baseline 引擎

选择复用 `run_real_business_corpus_golden_cases` 与现有 source-by-source decision logic，而不是新建另一套判定引擎。

原因：

- 失败问题包仍然是 real-business aggregate evidence 的一种变体。
- 复用当前逻辑可以确保 `go/review/blocked` 语义一致。
- 后续不同问题包之间也更容易横向比较。

### 2. 为失败问题补充 `question_origin` / `observed_failure` / `notes`

仅用 `failure_mode` 不足以表达问题来源和上下文，所以新增：

- `question_origin`
- `observed_failure`
- `notes`

这样后续看到 `review` 时，可以判断它是：

- 已接受的真实失败候选
- 真实边界问题
- 跨域陷阱问题

而不需要回头人工翻聊天记录。

### 3. 失败问题包与常规 aggregate baseline 分开导出

不把失败问题包直接塞进 `real-business-corpus-golden-cases.json`，而是单独导出：

- `real-failed-question-pack.json`
- `real-failed-question-pack.md`

原因：

- 常规 aggregate baseline 代表当前真实业务覆盖面
- 失败问题包代表未来技术选择的 review 输入

二者职责不同，混在一个文件里会降低可读性，也容易误导后续决策。

## Risks / Trade-offs

- [失败问题包中的问题并非全部都失败] → 这是允许的；该问题包的价值是沉淀困难/边界/失败候选，而不是保证全部 `review`。
- [独立报告与常规 aggregate baseline 口径漂移] → 复用同一评估引擎，避免逻辑分叉。
- [问题来源字段长期缺失或随意填写] → 先把字段纳入 fixture schema 和报告汇总，让后续补充来源信息变成显式工作，而不是隐式习惯。
