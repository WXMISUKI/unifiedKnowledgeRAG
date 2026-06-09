## Context

项目已经完成 company profile baseline、第二真实业务 source 扩展、failure-mode 分类、markdown provenance diagnostics alignment，以及 negative-control hardening。当前 aggregate baseline 已回到 `go`。结合项目路线图和 `RAG_Techniques` 经验，下一步应优先扩大真实业务 breadth，而不是在没有新 failure 证据时引入 query rewrite、rerank、hybrid retrieval、RAPTOR 或 GraphRAG。

`logistics_faq` 已经是 provider 中现成可用的轻量 source，并且与现有公司画像/退款政策形成不同业务域。它适合作为第三个真实业务 source，用来覆盖：

- 物流流程问题
- 精确标识符问题
- 新业务域的 expected-empty negative control

## Goals / Non-Goals

**Goals:**

- 将 aggregate real-business baseline 扩展到第三个真实业务 source。
- 在不改变 runtime defaults 的前提下，增加新的业务问法覆盖。
- 继续用 source-by-source conservative evaluation 暴露真实 failure evidence。
- 保持现有报告、分类和 recommended actions 机制可复用。

**Non-Goals:**

- 不引入 query rewrite、HyDE、HyPE。
- 不引入 rerank、fusion/hybrid retrieval。
- 不调整 chunking default。
- 不引入 GraphRAG、RAPTOR、Self-RAG、CRAG。
- 不把 caller/control-plane 职责移入 provider。

## Decisions

### 1. 选择 `logistics_faq` 作为第三个真实业务 source

原因：

- 已经存在于 provider 的 lightweight source catalog 中。
- 与现有两个 source 形成新业务域，有利于做 breadth-first 验证。
- 可以同时覆盖流程型、精确标识型和 expected-empty 问题。

不选择直接新增更复杂外部 parser/source 的原因：

- 当前目标是扩展真实 baseline 覆盖，而不是打开新的 ingestion/ownership 工作流。
- 用现成 source 能把切片控制在最小范围。

### 2. 新增 case 仍坚持“answerable + negative control”成对设计

每个新 source 至少包含：

- answerable 流程/操作问题
- answerable 精确标识问题
- expected-empty negative control

这样能延续已有 evidence gate，避免只用“能回答的问题”堆高表面通过率。

### 3. 成功标准以 aggregate breadth 扩展为主，不以局部优化为主

本次切片的成功标准是：

- `source_count` 增加到 3
- aggregate 报告仍然 `go`，或者产生新的清晰 failure class

而不是为了追求更高 hit 数或更多返回 chunk 去做局部检索微调。

## Risks / Trade-offs

- [选中的物流问题过于依赖精确措辞] → 组合一个流程型问题和一个精确标识问题，避免只验证 exact-term lookup。
- [第三 source 扩展后 aggregate 重新进入 review] → 接受这个结果，把它视为下一阶段真实 failure evidence，而不是立即升级到高级策略。
- [fake test client 与真实 fixture 不一致] → 在测试里同步加入 `logistics_faq` 的最小 source/register/citation 映射，保持 aggregate 行为可验证。
