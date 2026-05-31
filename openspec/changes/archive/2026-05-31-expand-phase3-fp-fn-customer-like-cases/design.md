## Context

项目路线图要求 Phase 3 通过证据推进而非局部优化。当前基线可用，但在客户化误召回/漏召回评审上样例密度不足。

## Goals / Non-Goals

**Goals**

- 扩充最小必要的客户化 false-positive / false-negative 样例。
- 保持 benchmark 证据链同步更新，便于后续 gate 评审。
- 全程 evaluation-only，不修改运行时默认行为。

**Non-Goals**

- 不引入新检索后端、重排器、GraphRAG 执行。
- 不修改 Provider HTTP 合约与控制面职责边界。
- 不做自动 promotion 判定。

## Decisions

- 继续复用 canonical baseline fixture：`tests/fixtures/retrieval_benchmark_cases.json`。
- 新增样例保持与现有业务语境一致（退款/物流域），避免引入重型外部依赖。
- 刷新 `fixture-chinese-seed-baseline` 证据，确保 handoff 与评审读到的是最新基线。

## Risks / Trade-offs

- 样例数量增加会改变汇总统计，需要同步更新断言与证据文件。
- 基线仍使用 fixture 后端，指标可能保持满分；这符合当前“证据准备”阶段定位，不做默认提升依据。
