## Why

当前项目已经有多类 source evaluation artifacts：

- single-source baseline
- aggregate breadth baseline
- failed-question pack
- confirmation pack

这些 artifact 已经能支撑我们自己判断下一步，但它们还没有被统一投影成 provider 级通用视图。对于一个通用 RAG provider 来说，下一阶段更需要的是“任何新 source 或新调用方都能理解当前有哪些 evaluation gates、各自状态如何、下一条建议 gate 是什么”，而不是继续围绕某个具体业务 source 做专项 hardening。

结合 `RAG_Techniques` 的经验，这一步应该先标准化 evaluation gate 的公共视图，让后续 query rewrite、rerank、hybrid retrieval 或 GraphRAG 候选都必须站在统一 catalog 之上，而不是散落在多个脚本和报告中。

## What Changes

- 新增一个通用的 source evaluation pack catalog。
- 把现有 business-rag evaluation artifacts 统一映射为公共条目：
  - `pack_id`
  - `pack_type`
  - `source_scope`
  - `decision`
  - `case_count`
  - `recommended_next_gate`
- 提供统一 JSON/Markdown 目录报告，供后续 source 接入、调用方复核和策略候选门使用。
- 保持现有 baseline / failed-pack / confirmation 的具体导出逻辑不变，不改变 runtime defaults。

## Capabilities

### New Capabilities

- `local-business-rag-golden-cases`: provider 可以导出一个统一的 evaluation pack catalog，帮助调用方和维护者在不读取各个独立报告细节的情况下，快速理解当前 pack 全景与下一步 gate。

### Modified Capabilities

- None.

## Impact

- Affected code: `app/services/source_evaluation_pack_catalog.py`
- Affected scripts: `scripts/export_source_evaluation_pack_catalog.py`
- Affected tests: `tests/test_source_evaluation_pack_catalog.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.json`
  - `docs/local-run/business-rag-golden-cases/source-evaluation-pack-catalog.md`
