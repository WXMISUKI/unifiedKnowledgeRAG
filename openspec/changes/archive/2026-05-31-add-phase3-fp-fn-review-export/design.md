## Context

Phase 3 当前重点是证据驱动的评审，而不是运行时默认提升。已有 benchmark 报告可反映质量，但“误召回/漏召回”需要手工筛读 case 明细，效率较低。

## Goals / Non-Goals

**Goals**

- 从现有 benchmark 证据中提取 FP/FN 风险摘要。
- 输出简洁 JSON/Markdown，便于 handoff 与评审会议快速消费。
- 维持本地、只读、可重复执行。

**Non-Goals**

- 不修改检索逻辑、阈值、后端或 reranker。
- 不新增 provider HTTP API。
- 不自动做 runtime promotion 决策。

## Decisions

- 新增独立服务模块 `phase3_fp_fn_review.py`，避免影响现有 benchmark 核心流程。
- 默认输入路径为中文 seed 基线 evidence JSON。
- FP/FN 判定规则：
  - FP：`expect_empty=true` 且返回了证据（`empty_query_handling=false` 或 `returned_citations` 非空）
  - FN：`expect_empty=false` 且未命中预期（`hit_at_k=false` 或 `citation_match=false`）

## Risks / Trade-offs

- 依赖 benchmark evidence JSON 的字段稳定性；若字段缺失则快速失败并提示。
- 该导出是评审视图，不是 runtime gate 引擎，需在文档中明确边界。
