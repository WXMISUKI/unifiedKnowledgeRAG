## Why

当前 aggregate real-business baseline 已经在三个真实业务 source 上保持 `go`，说明继续只扩正常通过样本，会逐渐降低新 failure 暴露效率。现在需要单独建立一个“真实失败问题包 baseline”，把真实失败候选、边界问题和跨域陷阱问题沉淀为可复用评估资产，用它来驱动后续 query rewrite、rerank、hybrid retrieval 或其他高级技术是否值得进入候选门。

## What Changes

- 新增一个独立于常规 aggregate baseline 的真实失败问题包 fixture 与导出脚本。
- 扩展 aggregate case schema，支持记录 `question_origin`、`observed_failure` 和 `notes` 等失败问题上下文。
- 在失败问题包报告中输出 `question_origin_summary`，让后续技术决策能区分真实失败候选、边界问题和跨域陷阱。
- 保持现有 retrieval/runtime defaults 不变，仅将新问题包作为 evidence-only review 输入。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-business-rag-golden-cases`: 扩展 real-business aggregate baseline，使其可以承载独立的真实失败问题包 fixture、失败问题来源元数据，以及面向 failure-driven 下阶段选择的独立导出报告。

## Impact

- Affected code: `app/services/local_business_rag_golden_cases.py`
- Affected scripts: `scripts/export_real_failed_question_pack_golden_cases.py`
- Affected tests: `tests/test_real_failed_question_pack_golden_cases.py`
- Affected artifacts: `docs/local-run/business-rag-golden-cases/real-failed-question-pack.fixture.json`, `docs/local-run/business-rag-golden-cases/real-failed-question-pack.json`, `docs/local-run/business-rag-golden-cases/real-failed-question-pack.md`
