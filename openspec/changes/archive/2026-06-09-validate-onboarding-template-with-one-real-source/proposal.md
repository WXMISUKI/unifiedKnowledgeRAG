## Why

我们已经完成了：

- source evaluation pack catalog
- source evaluation pack onboarding 模板

但这两者还主要证明“框架存在”，还没有证明“一个新的真实 source 能低成本进入这条闭环”。对于通用 RAG provider 来说，下一阶段最重要的不是继续优化某个旧 case，而是验证模板化接入是否真的可落地。

`split_refund_policy_docs` 是一个合适的真实 source 验证对象：

- 它已有真实 markdown source 文件
- 它尚未进入当前 business-rag baseline 主闭环
- 它足够轻量，不会把项目拖入 parser、GraphRAG 或高级检索策略

因此，本次 change 的目标是用这个 source 走一遍模板化接入的最小验证路径。

## What Changes

- 为 `split_refund_policy_docs` 提供最小 provider 可见性，使其可被本地 baseline 验证使用。
- 用 onboarding helper 为该 source 生成模板，并填充一个最小真实 baseline fixture。
- 导出该 source 的真实 baseline 报告，作为模板链路可用性的验证证据。
- 保持 catalog、runtime defaults 和高级检索策略不变。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `local-business-rag-golden-cases`: 证明新的真实 source 可以通过标准化 onboarding 模板进入最小 baseline 验证路径，而不需要围绕旧 source 手工拼装全部评估资产。

## Impact

- Affected code:
  - `app/services/source_catalog.py`
  - `app/services/source_document_manifest.py`
  - `app/services/document_retriever.py`
- Affected scripts:
  - `scripts/export_split_refund_onboarding_validation.py`
- Affected tests:
  - `tests/test_split_refund_onboarding_validation.py`
- Affected artifacts:
  - `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/baseline-pack.fixture.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/split-refund-local-business-rag-golden-cases.json`
  - `docs/local-run/business-rag-golden-cases/onboarding/split_refund_policy_docs/split-refund-local-business-rag-golden-cases.md`
